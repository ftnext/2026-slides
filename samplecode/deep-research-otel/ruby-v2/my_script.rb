#!/usr/bin/env ruby
# frozen_string_literal: true

require 'opentelemetry/sdk'
require_relative './instrumentor'
require_relative './deep_research_lib'

USER_QUERY = 'ミリオンライブのエミリー・スチュアートさんの2025年の活躍を調べて教えて'

ENV['OTEL_TRACES_EXPORTER'] ||= 'console'
ENV['OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT'] ||= 'true'

OpenTelemetry::SDK.configure do |c|
  c.service_name = 'my-google-genai-deep-research'
end

MyGoogleGenai::Instrumentation::Instrumentor.new.instrument

def resolve_api_key
  ENV['GEMINI_API_KEY'] || ENV['GOOGLE_API_KEY'] || ''
end

def main
  api_key = resolve_api_key
  if api_key.empty?
    warn('API key not found. Set GEMINI_API_KEY/GOOGLE_API_KEY environment variable.')
    return 2
  end

  config = Config.new(
    topic_generator_model_name: 'gemini-2.5-flash',
    topic_researcher_model_name: 'gemini-2.5-flash',
    research_synthesizer_model_name: 'gemini-2.5-flash',
    num_topics: 5,
    excluded_topics: [],
    max_parallel_research: 5,
    timeout_sec: 30
  )

  result = ResearchAgent.new(api_key: api_key, config: config).run(USER_QUERY)
  puts result
  0
rescue StandardError => e
  warn("Failed: #{e}")
  1
end

exit(main) if __FILE__ == $PROGRAM_NAME
