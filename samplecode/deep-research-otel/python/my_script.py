# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai>=1.65.0",
# ]
# ///
import argparse
import asyncio

from deep_research_lib import Config, ResearchAgent


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
