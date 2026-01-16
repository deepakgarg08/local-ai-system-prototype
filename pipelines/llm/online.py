# pipelines/llm/online.py

from .base import BaseLLM


class OnlineLLM(BaseLLM):
    """
    Adapter for online LLM APIs (OpenAI, Anthropic, etc.).
    """

    def __init__(self, provider: str = "generic"):
        self.provider = provider

    def generate(self, prompt: str) -> str:
        # TODO: replace with actual API call
        return (
            "[ONLINE LLM PLACEHOLDER RESPONSE]\n\n"
            f"Provider: {self.provider}\n"
            f"Prompt length: {len(prompt)} characters."
        )
