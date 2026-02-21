require "faraday"
require "json"
require "opentelemetry/sdk"
require "opentelemetry/instrumentation/faraday"

ENV["OTEL_TRACES_EXPORTER"] = "console"
OpenTelemetry::SDK.configure do |c|
  c.use 'OpenTelemetry::Instrumentation::Faraday'
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

api_key = ENV["GEMINI_API_KEY"]
conn = Faraday.new(
  url: "https://generativelanguage.googleapis.com"
) do |f|
  f.adapter Faraday.default_adapter
end
conn.builder.insert_after(
  OpenTelemetry::Instrumentation::Faraday::Middlewares::Old::TracerMiddleware,
  OtelBodyCaptureMiddleware
)

response = conn.post(
  "/v1beta/models/gemini-3-flash-preview:generateContent"
) do |req|
  req.headers["Content-type"] = "application/json"
  req.headers["x-goog-api-key"] = api_key
  req.body = {
    contents: [
      {
        parts: [
          { text: "OpenTelemetry について短い詩を書いてください。" }
        ]
      }
    ]
  }.to_json
end

# json = JSON.parse(response.body)
# puts json["candidates"][0]["content"]["parts"][0]["text"]
