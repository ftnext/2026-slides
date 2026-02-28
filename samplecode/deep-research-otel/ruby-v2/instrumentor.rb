# frozen_string_literal: true

require 'opentelemetry-api'
require_relative 'client'

module MyGoogleGenai
  module Instrumentation
    class Instrumentor
      CAPTURE_CONTENT_ENV = 'OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT'

      def initialize(tracer: nil)
        @tracer = tracer || OpenTelemetry.tracer_provider.tracer('my_google_genai', '0.1.0')
        @instrumented = false
        @original_generate_content = nil
      end

      def instrument
        return false if @instrumented

        patch_generate_content
        @instrumented = true
      end

      def uninstrument
        return false unless @instrumented
        return false unless @original_generate_content

        original = @original_generate_content
        MyGoogleGenai::Client.define_method(:generate_content, original)

        @original_generate_content = nil
        @instrumented = false
        true
      end

      private

      def patch_generate_content
        @original_generate_content = MyGoogleGenai::Client.instance_method(:generate_content)
        original = @original_generate_content
        tracer = @tracer
        capture_content_env = CAPTURE_CONTENT_ENV
        prompt_text_extractor = lambda do |contents|
          return contents.to_s unless contents.is_a?(Array)

          contents.flat_map do |entry|
            parts = (entry[:parts] || entry['parts'] || [])
            parts.filter_map { |part| part[:text] || part['text'] }
          end.join("\n")
        end

        MyGoogleGenai::Client.define_method(:generate_content) do |**kwargs|
          model = instance_variable_get(:@model)
          capture_content = ENV.fetch(capture_content_env, 'false').downcase == 'true'

          attributes = {
            'gen_ai.system' => 'gemini',
            'gen_ai.operation.name' => 'generate_content',
            'gen_ai.request.model' => model
          }

          tracer.in_span("generate_content #{model}", attributes: attributes, kind: :client) do |span|
            if capture_content
              prompt_text = prompt_text_extractor.call(kwargs[:contents])
              span.add_event('gen_ai.user.message', attributes: { 'content' => prompt_text }) unless prompt_text.empty?
            end

            begin
              response = original.bind(self).call(**kwargs)

              if capture_content
                response_text = extract_text(response)
                span.add_event('gen_ai.choice', attributes: { 'content' => response_text }) unless response_text.empty?
              end

              response
            rescue StandardError => e
              span.set_attribute('error.type', e.class.name)
              span.record_exception(e)
              span.status = OpenTelemetry::Trace::Status.error(e.message)
              raise
            end
          end
        end
      end
    end
  end
end
