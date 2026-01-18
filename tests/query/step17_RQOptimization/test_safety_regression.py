# tests/query/step17_RQOptimization/test_safety_regression.py

from pipelines.query.run_rag import run_rag


def test_llm_not_called_when_grounding_fails(monkeypatch):
    """
    STEP 17 regression test:
    If grounding fails, the LLM must never be called.
    """

    # Mock retriever to return irrelevant content
    monkeypatch.setattr(
        "pipelines.query.run_rag.retrieve_context_with_scores",
        lambda *args, **kwargs: [("irrelevant text", 0.01)],
    )

    # Force grounding failure
    monkeypatch.setattr(
        "pipelines.query.run_rag.is_context_relevant",
        lambda *args, **kwargs: False,
    )

    # Track LLM calls explicitly
    class FakeLLM:
        def generate(self, prompt):
            raise AssertionError("LLM should not be called")

    monkeypatch.setattr(
        "pipelines.query.run_rag.get_llm",
        lambda: FakeLLM(),
    )

    result = run_rag("irrelevant query")

    assert result.answer is None
