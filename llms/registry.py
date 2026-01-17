# llms/registry.py

from llms.base import BaseLLM
from llms.ollama import OllamaLLM

DEFAULT_OLLAMA_MODEL = "deepseek-coder:6.7b"
def get_llm() -> BaseLLM:
    """
    Unified entry point for obtaining an LLM instance.

    Current behavior:
        - Always returns a local Ollama-backed LLM.

    Design notes:
        - Pipelines must never import concrete LLM implementations directly.
        - This function is the single choke point for future model selection.
        - Any failure here should be explicit and loud.
    """
    return OllamaLLM(model=DEFAULT_OLLAMA_MODEL)
