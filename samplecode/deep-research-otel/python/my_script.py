# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai>=1.65.0",
#     "opentelemetry-instrumentation-google-genai>=0.7b0",
#     "opentelemetry-sdk>=1.39.1",
# ]
# ///
import argparse
import asyncio
import os

from opentelemetry._logs import set_logger_provider
from opentelemetry.instrumentation.google_genai import GoogleGenAiSdkInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogRecordExporter,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import get_tracer_provider, set_tracer_provider

from deep_research_lib import Config, ResearchAgent

os.environ["OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"] = "true"

set_tracer_provider(TracerProvider())
get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

provider = LoggerProvider()
provider.add_log_record_processor(BatchLogRecordProcessor(ConsoleLogRecordExporter()))
set_logger_provider(provider)

GoogleGenAiSdkInstrumentor().instrument()


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    args = parser.parse_args()

    config = Config(
        topic_generator_model_name="gemini-2.5-flash",
        topic_researcher_model_name="gemini-2.5-flash",
        research_synthesizer_model_name="gemini-2.5-flash",
        num_topics=5,
        max_parallel_research=5,
    )
    agent = ResearchAgent(config=config)

    result = await agent.run(args.query)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
