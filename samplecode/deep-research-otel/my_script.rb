#!/usr/bin/env ruby
# frozen_string_literal: true

require "faraday"
require "json"
require "opentelemetry/sdk"
require "opentelemetry/instrumentation/faraday"
require_relative "./deep_research_lib"

USER_QUERY = "ミリオンライブのエミリー・スチュアートさんの2025年の活躍を調べて教えて"

ENV["OTEL_TRACES_EXPORTER"] ||= "console"
OpenTelemetry::SDK.configure do |c|
  c.use "OpenTelemetry::Instrumentation::Faraday"
end

class OtelBodyCaptureMiddleware < Faraday::Middleware
  def call(env)
    span = OpenTelemetry::Trace.current_span
    if span&.recording?
      body = env.body
      body_str = body.is_a?(String) ? body : JSON.generate(body)
      span.set_attribute("http.request.body", body_str)
    end

    response = @app.call(env)

    if span&.recording?
      span.set_attribute("http.response.body", response.body.to_s)
    end
    response
  end
end

def resolve_api_key
  ENV["GEMINI_API_KEY"] || ENV["GOOGLE_API_KEY"] || ""
end

def attach_faraday_otel_middlewares(conn)
  conn.builder.insert_after(
    OpenTelemetry::Instrumentation::Faraday::Middlewares::Old::TracerMiddleware,
    OtelBodyCaptureMiddleware
  )
end

def main
  api_key = resolve_api_key
  if api_key.empty?
    warn("API key not found. Set GEMINI_API_KEY/GOOGLE_API_KEY environment variable.")
    return 2
  end

  config = Config.new(
    topic_generator_model_name: "gemini-2.5-flash",
    topic_researcher_model_name: "gemini-2.5-flash",
    research_synthesizer_model_name: "gemini-2.5-flash",
    num_topics: 5,
    max_parallel_research: 5,
  )

  agent = ResearchAgent.new(api_key: api_key, config: config) do |conn|
    attach_faraday_otel_middlewares(conn)
  end
  result = agent.run(USER_QUERY)
  puts result
  0
rescue StandardError => e
  warn("Failed: #{e}")
  1
end

exit(main) if __FILE__ == $PROGRAM_NAME
