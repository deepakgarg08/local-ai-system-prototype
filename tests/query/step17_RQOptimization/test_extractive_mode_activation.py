# tests/query/step17_RQOptimization/test_extractive_mode_activation.py

from unittest.mock import Mock

from pipelines.query.run_rag import run_rag


def test_extractive_mode_activated_for_small_corpus_single_chunk(monkeypatch, real_retrieval_item,):
    """
    STEP 17:
    Small corpus + single short chunk → extractive-only mode must be used.
    """

    # Mock retriever: single strong but short chunk
    monkeypatch.setattr(
        "pipelines.query.run_rag.retrieve_context_with_scores",
        lambda *args, **kwargs: [real_retrieval_item],
    )

    # Mock LLM to capture prompt
    mock_llm = Mock()
    mock_llm.generate.return_value = "Short but relevant paragraph."

    monkeypatch.setattr(
        "pipelines.query.run_rag.get_llm",
        lambda: mock_llm,
    )

    result = run_rag("test query")

    assert result.answer is not None

    # Inspect the prompt passed to the LLM
    prompt_used = mock_llm.generate.call_args[0][0]
    assert "Answer ONLY by quoting or closely paraphrasing" in prompt_used
