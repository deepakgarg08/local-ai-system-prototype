# configs/runtime.py

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str


def load_llm_config() -> LLMConfig:
    """
    Load LLM configuration from environment variables.

    Required variables:
        LLM_PROVIDER: "ollama" or "openai"
        LLM_MODEL: model name for the selected provider
    """
    provider = os.getenv("LLM_PROVIDER")
    model = os.getenv("LLM_MODEL")

    if not provider:
        raise RuntimeError("LLM_PROVIDER is not set")

    if not model:
        raise RuntimeError("LLM_MODEL is not set")

    provider = provider.lower()

    if provider not in {"ollama", "openai"}:
        raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider}")

    return LLMConfig(provider=provider, model=model)
