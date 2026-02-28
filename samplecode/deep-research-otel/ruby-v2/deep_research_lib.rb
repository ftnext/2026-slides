# frozen_string_literal: true

require 'json'
require 'thread'
require_relative './client'

TOPIC_GENERATION_PREAMBLE = <<~TEXT
  You are an expert at generating topics for research, based on the user's content.

  Your first task is to devise a number of concrete research areas needed to address the user's content.

  E.g., if the user's content was 'Starting a vegetable garden in my small backyard in London', you would provide up to {num_topics} topics to be individually researched, such as "what vegetables can grow in the London climate?", and "vegetables that can grow with limited space".

  E.g. for "vegetables that can grow with limited space", the 'relationship' could be 'We need to know which vegetables can grow in limited space, given the user wants to start a vegetable garden in their **small** backyard'.
TEXT

TOPIC_RESEARCH_PREAMBLE = <<~TEXT
  You are an expert at performing "Deep Research" for users.

  Return your detailed research on this topic, in relation to the user's input.

  Your research will be collated & provided to another expert, who will combine the research from various topic areas to provide one cohesive answer to the user; so DO NOT exceed the scope of the topic you have been asked to investigate.

  DO NOT include citation numbers in your research.
TEXT

SYNTHESIS_PREAMBLE = <<~TEXT
  You are an expert at evaluating research results and synthesizing them into a single coherent piece of research.

  You will be provided with the user's original content, and the research that has been performed on various topics related to that content.

  Please produce a single piece of synthesized research, which collates the provided research into a single coherent piece, which can be used to directly answer the user's original content.

  Make sure to reference each of the topics researched at least once in your synthesis.
TEXT

Topic = Struct.new(:topic, :relationship_to_user_content, :research_text, keyword_init: true)
Config = Struct.new(
  :topic_generator_model_name,
  :topic_researcher_model_name,
  :research_synthesizer_model_name,
  :num_topics,
  :excluded_topics,
  :max_parallel_research,
  :timeout_sec,
  keyword_init: true
)

class ResearchAgent
  def initialize(api_key:, config:)
    @api_key = api_key
    @config = config
  end

  def run(user_content)
    topics = generate_topics(user_content)
    researched = research_topics(user_content, topics)
    synthesize(user_content, researched)
  end

  private

  def generate_topics(user_content)
    prompt_parts = [
      TOPIC_GENERATION_PREAMBLE,
      "Please provide exactly #{@config.num_topics} research topics, along with each topic's relationship to the user prompt."
    ]
    if @config.excluded_topics && !@config.excluded_topics.empty?
      prompt_parts << "Here is a list of topics that should be excluded: #{@config.excluded_topics.join(', ')}"
    end

    prompt_parts.concat(
      [
        'You will now be provided with the user content.',
        'User content:',
        user_content,
        <<~TEXT
          Return your response as Topics JSON in the format below.

          You MUST return exactly #{@config.num_topics} topics.

          Topic
            topic: str
            relationship_to_user_content: str

          Topics
            list[Topic]

          Your JSON:
        TEXT
      ]
    )

    response = generate_content(
      @config.topic_generator_model_name,
      contents: [{ role: 'user', parts: [{ text: prompt_parts.join("\n\n") }] }],
      generation_config: { responseMimeType: 'application/json' }
    )
    raw_text = extract_text(response, @config.topic_generator_model_name)
    normalize_topics(parse_topics_json(raw_text), @config.num_topics)
  end

  def research_topics(user_content, topics)
    queue = Queue.new
    topics.each_with_index { |topic, index| queue << [index, topic] }
    results = Array.new(topics.length)
    errors = []
    errors_mutex = Mutex.new

    worker_count = [[1, @config.max_parallel_research.to_i].max, topics.length].min
    workers = Array.new(worker_count) do
      Thread.new do
        loop do
          item = begin
            queue.pop(true)
          rescue ThreadError
            nil
          end
          break if item.nil?

          index, topic = item
          begin
            research = research_one_topic(user_content, topic)
            results[index] = Topic.new(
              topic: topic.topic,
              relationship_to_user_content: topic.relationship_to_user_content,
              research_text: research
            )
          rescue StandardError => e
            errors_mutex.synchronize { errors << e }
          end
        end
      end
    end

    workers.each(&:join)
    raise errors.first unless errors.empty?

    results
  end

  def research_one_topic(user_content, topic)
    prompt = <<~TEXT
      #{TOPIC_RESEARCH_PREAMBLE}

      User content:
      #{user_content}

      Topic to research:
      ## #{topic.topic}
      *#{topic.relationship_to_user_content}*

      Your research:
    TEXT

    response = generate_content(
      @config.topic_researcher_model_name,
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      tools: [{ googleSearch: {} }]
    )
    extract_text(response, @config.topic_researcher_model_name).strip
  end

  def synthesize(user_content, researched_topics)
    research_blob = researched_topics.map { |topic| topic_to_markdown(topic) }.join("\n\n")
    prompt = <<~TEXT
      #{SYNTHESIS_PREAMBLE}

      User content:
      #{user_content}

      Research text:
      #{research_blob}

      Your synthesized research:
    TEXT

    response = generate_content(
      @config.research_synthesizer_model_name,
      contents: [{ role: 'user', parts: [{ text: prompt }] }]
    )
    extract_text(response, @config.research_synthesizer_model_name).strip
  end

  def generate_content(model, contents:, generation_config: nil, tools: nil)
    client = MyGoogleGenai::Client.new(
      api_key: @api_key,
      model: model,
      timeout_sec: @config.timeout_sec || 30
    )
    client.generate_content(
      contents: contents,
      generation_config: generation_config,
      tools: tools
    )
  rescue MyGoogleGenai::Error => e
    raise MyGoogleGenai::Error, "#{model}: #{e.message}"
  end

  def extract_text(response, model)
    MyGoogleGenai::Client.new(api_key: @api_key, model: model).extract_text(response)
  end

  def extract_json_array(raw)
    stripped = raw.strip
    return stripped if stripped.start_with?('[') && stripped.end_with?(']')

    match = raw.match(/\[[\s\S]*\]/)
    raise ArgumentError, 'JSON array not found in model output.' unless match

    match[0]
  end

  def parse_topics_json(raw_text)
    data = JSON.parse(extract_json_array(raw_text))
    data.each_with_index.map do |item, i|
      raise ArgumentError, "Topic at index #{i} is not an object." unless item.is_a?(Hash)

      topic = item.fetch('topic', '').to_s.strip
      topic = "Untitled topic #{i + 1}" if topic.empty?
      relationship = item.fetch('relationship_to_user_content', '').to_s.strip
      relationship = 'No relationship explanation provided.' if relationship.empty?
      Topic.new(topic: topic, relationship_to_user_content: relationship)
    end
  end

  def normalize_topics(topics, num_topics)
    return topics if topics.length == num_topics
    return topics.first(num_topics) if topics.length > num_topics

    padded = topics.dup
    while padded.length < num_topics
      i = padded.length + 1
      padded << Topic.new(
        topic: "Additional topic #{i}",
        relationship_to_user_content: 'Added because topic count was lower than requested.'
      )
    end
    padded
  end

  def topic_to_markdown(topic)
    research = topic.research_text.to_s.strip
    if research.empty?
      "## #{topic.topic}\n*#{topic.relationship_to_user_content}*"
    else
      "## #{topic.topic}\n*#{topic.relationship_to_user_content}*\n\n### Research\n\n#{research}"
    end
  end
end
