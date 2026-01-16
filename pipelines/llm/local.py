# pipelines/llm/local.py

from .base import BaseLLM


class LocalLLM(BaseLLM):
    """
    Adapter for local LLMs.
    """

    def __init__(self, model_name: str = "local-model"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        # TODO: replace with actual local inference
        return (
            "[LOCAL LLM PLACEHOLDER RESPONSE]\n\n"
            f"Prompt received ({len(prompt)} characters)."
        )
