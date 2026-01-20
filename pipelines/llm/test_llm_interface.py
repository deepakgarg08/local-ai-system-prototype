# from llms.ollama import OllamaLLM

# llm = OllamaLLM(model="deepseek-coder:6.7b")

# response = llm.generate(
#     "Explain what a vector database is in one concise paragraph."
# )

# print(response)

#  Above was earlier smog test code to check if ollama llm was working fine.

# pipelines/llm/test_llm_interface.py

import pytest
from llms.registry import get_llm


def test_get_llm_fails_without_provider(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    with pytest.raises(RuntimeError):
        get_llm()


def test_get_llm_constructs_llm_object(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("LLM_MODEL", "dummy-model")

    llm = get_llm()

    # We only assert construction, not connectivity
    assert llm is not None
