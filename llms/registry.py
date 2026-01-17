# llms/registry.py

from llms.base import BaseLLM
from llms.ollama import OllamaLLM
from llms.openai import OpenAILLM
from configs.runtime import load_llm_config

def get_llm() -> BaseLLM:
    """
    Unified entry point for obtaining an LLM instance.

    Selection is config-driven and explicit.
    """
    cfg = load_llm_config()

    if cfg.provider == "ollama":
        return OllamaLLM(model=cfg.model)

    if cfg.provider == "openai":
        return OpenAILLM(model=cfg.model)

    # Defensive (should be unreachable)
    raise RuntimeError(f"Unhandled LLM provider: {cfg.provider}")
