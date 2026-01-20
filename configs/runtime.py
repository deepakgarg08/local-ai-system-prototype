# configs/runtime.py

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str


def _get_float_env(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        raise RuntimeError(f"{name} must be a float, got: {value}")


# STEP 20.5 — policy-level threshold for answer gating
RERANK_MIN_SCORE: float = _get_float_env("RERANK_MIN_SCORE", 0.5)


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
