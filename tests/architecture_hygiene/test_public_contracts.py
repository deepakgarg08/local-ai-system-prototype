from pipelines.query.run_rag import run_rag, RAGResult
from tests.fakes.fake_llm import FakeLLM


def test_run_rag_returns_structured_result(monkeypatch):
    """
    Public contract test:
    run_rag must return a structured RAGResult object,
    not raw strings or ad-hoc dictionaries.
    """

    fake_llm = FakeLLM(answer="safe answer")

    # Ensure run_rag does not touch real environment / registry
    monkeypatch.setattr(
        "pipelines.query.run_rag.get_llm",
        lambda: fake_llm,
    )

    result = run_rag("What is this system?")

    assert isinstance(result, RAGResult)
    assert result.query == "What is this system?"
    assert hasattr(result, "answer")
    assert hasattr(result, "confidence")
    assert hasattr(result, "sources")
