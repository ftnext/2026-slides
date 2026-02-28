# https://github.com/anthropics/anthropic-sdk-ruby/blob/main/examples/web_search.rb
require "anthropic"
require "opentelemetry/sdk"
require "opentelemetry/instrumentation/anthropic"
require "opentelemetry/instrumentation/net/http"

ENV["OTEL_TRACES_EXPORTER"] = "console"
OpenTelemetry::SDK.configure do |c|
  c.use "OpenTelemetry::Instrumentation::Net::HTTP"
  c.use "OpenTelemetry::Instrumentation::Anthropic"
end

anthropic = Anthropic::Client.new

message = anthropic.messages.create(
  model: "claude-haiku-4-5-20251001",
  max_tokens: 1024,
  messages: [{role: :user, content: "What's the weather in New York?"}],
  tools: [{name: "web_search", type: "web_search_20250305"}],
)

message
  .content
  .each do |content|
    case content
    when Anthropic::ServerToolUseBlock
      pp("Tool use: ---")
      pp(content.input)
    when Anthropic::WebSearchToolResultBlock
      pp("Search: ---")
      pp(content.content)
    when Anthropic::TextBlock
      pp("Text: ---")
      pp(content.text)
    end
  end

pp("Input tokens: #{message.usage.input_tokens}")

pp("Output tokens: #{message.usage.output_tokens}")
