"""Research agent using google-genai directly.

Based on: https://github.com/google-gemini/genai-processors/tree/main/examples/research
"""

from __future__ import annotations

import asyncio
import dataclasses
import json
import re
import sys
from typing import Any

from google import genai
from google.genai import types

TOPIC_GENERATION_PREAMBLE = """You are an expert at generating topics for research, based on the user's content.

Your first task is to devise a number of concrete research areas needed to address the user's content.

E.g., if the user's content was 'Starting a vegetable garden in my small backyard in London', you would provide up to {num_topics} topics to be individually researched, such as "what vegetables can grow in the London climate?", and "vegetables that can grow with limited space".

E.g. for "vegetables that can grow with limited space", the 'relationship' could be 'We need to know which vegetables can grow in limited space, given the user wants to start a vegetable garden in their **small** backyard'.
"""


TOPIC_RESEARCH_PREAMBLE = """You are an expert at performing "Deep Research" for users.

Return your detailed research on this topic, in relation to the user's input.

Your research will be collated & provided to another expert, who will combine the research from various topic areas to provide one cohesive answer to the user; so DO NOT exceed the scope of the topic you have been asked to investigate.

DO NOT include citation numbers in your research.
"""


SYNTHESIS_PREAMBLE = """You are an expert at evaluating research results and synthesizing them into a single coherent piece of research.

You will be provided with the user's original content, and the research that has been performed on various topics related to that content.

Please produce a single piece of synthesized research, which collates the provided research into a single coherent piece, which can be used to directly answer the user's original content.

Make sure to reference each of the topics researched at least once in your synthesis.
"""


@dataclasses.dataclass(frozen=True)
class Topic:
    topic: str
    relationship_to_user_content: str
    research_text: str | None = None


@dataclasses.dataclass
class Config:
    topic_generator_model_name: str = "gemini-2.5-flash"
    topic_researcher_model_name: str = "gemini-2.5-flash"
    research_synthesizer_model_name: str = "gemini-2.5-flash"
    num_topics: int = 5
    excluded_topics: list[str] = dataclasses.field(default_factory=list)
    max_parallel_research: int = 5
    request_timeout_ms: int = 120_000
    retry_attempts: int = 6


class ResearchAgent:
    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.client = genai.Client(
            http_options=types.HttpOptions(
                timeout=self.config.request_timeout_ms,
                retry_options=types.HttpRetryOptions(
                    attempts=self.config.retry_attempts
                ),
            ),
        )

    async def run(self, user_content: str, verbose: bool = False) -> str:
        topics = await self.generate_topics(user_content, verbose=verbose)
        researched_topics = await self.research_topics(
            user_content, topics, verbose=verbose
        )
        return await self.synthesize(user_content, researched_topics, verbose=verbose)

    async def generate_topics(
        self, user_content: str, verbose: bool = False
    ) -> list[Topic]:
        prompt_parts = [
            TOPIC_GENERATION_PREAMBLE,
            (
                f"Please provide exactly {self.config.num_topics} research topics, "
                "along with each topic's relationship to the user prompt."
            ),
        ]
        if self.config.excluded_topics:
            prompt_parts.append(
                "Here is a list of topics that should be excluded: "
                + ", ".join(self.config.excluded_topics)
            )
        prompt_parts.append("You will now be provided with the user content.")
        prompt_parts.append("User content:")
        prompt_parts.append(user_content)
        prompt_parts.append(
            f"""Return your response as Topics JSON in the format below.

You MUST return exactly {self.config.num_topics} topics.

Topic
  topic: str
  relationship_to_user_content: str

Topics
  list[Topic]

Your JSON:
"""
        )

        if verbose:
            print(
                f"[topic-generator] requesting {self.config.num_topics} topics...",
                file=sys.stderr,
            )

        response = await self.client.aio.models.generate_content(
            model=self.config.topic_generator_model_name,
            contents=["\n\n".join(prompt_parts)],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        raw_text = self._response_text(response)
        topics = self._parse_topics_json(raw_text)
        topics = self._normalize_topics(topics, self.config.num_topics)

        if verbose:
            print(f"[topic-generator] generated {len(topics)} topics", file=sys.stderr)
            for i, topic in enumerate(topics, start=1):
                print(f"  {i}. {topic.topic}", file=sys.stderr)

        return topics

    async def research_topics(
        self, user_content: str, topics: list[Topic], verbose: bool = False
    ) -> list[Topic]:
        semaphore = asyncio.Semaphore(max(1, self.config.max_parallel_research))

        async def _research_one(index: int, topic: Topic) -> Topic:
            async with semaphore:
                if verbose:
                    print(
                        f"[topic-researcher] ({index}/{len(topics)}) {topic.topic}",
                        file=sys.stderr,
                    )
                research_text = await self.research_one_topic(user_content, topic)
                return dataclasses.replace(topic, research_text=research_text)

        tasks = [
            asyncio.create_task(_research_one(i, t))
            for i, t in enumerate(topics, start=1)
        ]
        researched = await asyncio.gather(*tasks)
        return researched

    async def research_one_topic(self, user_content: str, topic: Topic) -> str:
        prompt = (
            f"{TOPIC_RESEARCH_PREAMBLE}\n\n"
            "User content:\n"
            f"{user_content}\n\n"
            "Topic to research:\n"
            f"## {topic.topic}\n"
            f"*{topic.relationship_to_user_content}*\n\n"
            "Your research:"
        )

        response = await self.client.aio.models.generate_content(
            model=self.config.topic_researcher_model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
            ),
        )
        return self._response_text(response).strip()

    async def synthesize(
        self, user_content: str, researched_topics: list[Topic], verbose: bool = False
    ) -> str:
        research_blob = "\n\n".join(
            self._topic_to_markdown(topic) for topic in researched_topics
        )
        prompt = (
            f"{SYNTHESIS_PREAMBLE}\n\n"
            "User content:\n"
            f"{user_content}\n\n"
            "Research text:\n"
            f"{research_blob}\n\n"
            "Your synthesized research:"
        )

        if verbose:
            print("[synthesizer] synthesizing final output...", file=sys.stderr)

        response = await self.client.aio.models.generate_content(
            model=self.config.research_synthesizer_model_name,
            contents=[prompt],
        )
        return self._response_text(response).strip()

    @staticmethod
    def _response_text(response: Any) -> str:
        text = getattr(response, "text", None)
        if text:
            return text
        candidates = getattr(response, "candidates", None) or []
        chunks: list[str] = []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            parts = getattr(content, "parts", None) or []
            for part in parts:
                part_text = getattr(part, "text", None)
                if part_text:
                    chunks.append(part_text)
        return "\n".join(chunks).strip()

    @staticmethod
    def _extract_json_array(raw: str) -> str:
        stripped = raw.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            return stripped
        match = re.search(r"\[[\s\S]*\]", raw)
        if not match:
            raise ValueError("JSON array not found in model output.")
        return match.group(0)

    def _parse_topics_json(self, raw_text: str) -> list[Topic]:
        json_array = self._extract_json_array(raw_text)
        data = json.loads(json_array)
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array for topics.")

        topics: list[Topic] = []
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(f"Topic at index {i} is not an object.")
            topic_val = str(item.get("topic", "")).strip()
            relationship_val = str(item.get("relationship_to_user_content", "")).strip()
            if not topic_val:
                topic_val = f"Untitled topic {i + 1}"
            if not relationship_val:
                relationship_val = "No relationship explanation provided."
            topics.append(
                Topic(
                    topic=topic_val,
                    relationship_to_user_content=relationship_val,
                )
            )
        return topics

    @staticmethod
    def _normalize_topics(topics: list[Topic], num_topics: int) -> list[Topic]:
        if len(topics) == num_topics:
            return topics
        if len(topics) > num_topics:
            return topics[:num_topics]
        # Fill missing topics with placeholders to keep contract.
        padded = list(topics)
        while len(padded) < num_topics:
            idx = len(padded) + 1
            padded.append(
                Topic(
                    topic=f"Additional topic {idx}",
                    relationship_to_user_content="Added because topic count was lower than requested.",
                )
            )
        return padded

    @staticmethod
    def _topic_to_markdown(topic: Topic) -> str:
        research = topic.research_text.strip() if topic.research_text else ""
        if research:
            return (
                f"## {topic.topic}\n"
                f"*{topic.relationship_to_user_content}*\n\n"
                f"### Research\n\n{research}"
            )
        return f"## {topic.topic}\n*{topic.relationship_to_user_content}*"
