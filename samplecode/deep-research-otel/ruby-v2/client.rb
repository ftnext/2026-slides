# frozen_string_literal: true

require 'json'
require 'faraday'

module MyGoogleGenai
  class Error < StandardError; end

  class Client
    API_BASE = 'https://generativelanguage.googleapis.com/v1beta'

    def initialize(api_key:, model: 'gemini-2.0-flash', base_url: API_BASE, timeout_sec: 30, connection: nil)
      @api_key = api_key
      @model = model
      @connection = connection || Faraday.new(url: base_url, request: { timeout: timeout_sec }) do |f|
        f.adapter Faraday.default_adapter
      end
    end

    # Sends a single Gemini generateContent request and returns parsed JSON Hash.
    def generate_content(contents:, system_instruction: nil, generation_config: nil, tools: nil)
      payload = { 'contents' => normalize_contents(contents) }
      payload['systemInstruction'] = normalize_system_instruction(system_instruction) if system_instruction
      payload['generationConfig'] = normalize_generation_config(generation_config) if generation_config
      payload['tools'] = normalize_tools(tools) if tools

      response = @connection.post("models/#{@model}:generateContent") do |req|
        req.params['key'] = @api_key
        req.headers['content-type'] = 'application/json'
        req.body = JSON.generate(payload)
      end

      body_hash = parse_json_body(response.body)
      return body_hash if response.status.between?(200, 299)

      error_message = body_hash.dig('error', 'message') || "HTTP #{response.status}"
      raise Error, error_message
    end

    # Best-effort helper to extract plain text from response payload.
    def extract_text(response_hash)
      candidates = response_hash.fetch('candidates', [])
      return '' if !candidates.is_a?(Array) || candidates.empty?

      parts = candidates.flat_map do |candidate|
        content = candidate['content'] || {}
        content.fetch('parts', [])
      end

      parts.filter_map { |part| part['text'] }.join("\n")
    end

    private

    def parse_json_body(body)
      return {} if body.nil? || body.empty?

      JSON.parse(body)
    rescue JSON::ParserError
      { 'raw_body' => body }
    end

    def normalize_contents(contents)
      return contents if contents.is_a?(Array)
      return [contents] if contents.is_a?(Hash)

      [{ role: 'user', parts: [{ text: contents.to_s }] }]
    end

    def normalize_system_instruction(system_instruction)
      return system_instruction if system_instruction.is_a?(Hash)

      { parts: [{ text: system_instruction.to_s }] }
    end

    def normalize_generation_config(generation_config)
      return generation_config unless generation_config.is_a?(Hash)

      result = generation_config.dup
      if result.key?(:response_mime_type) && !result.key?(:responseMimeType)
        result[:responseMimeType] = result.delete(:response_mime_type)
      end
      if result.key?('response_mime_type') && !result.key?('responseMimeType')
        result['responseMimeType'] = result.delete('response_mime_type')
      end
      result
    end

    def normalize_tools(tools)
      return tools if tools.is_a?(Array)

      [tools]
    end
  end
end
