require "faraday"
require "json"

api_key = ENV["GEMINI_API_KEY"]
conn = Faraday.new(
  url: "https://generativelanguage.googleapis.com"
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

json = JSON.parse(response.body)
puts json["candidates"][0]["content"]["parts"][0]["text"]
