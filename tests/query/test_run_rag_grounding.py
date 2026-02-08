# tests/query/test_run_rag_grounding.py

from unittest.mock import Mock, patch

from pipelines.query.run_rag import run_rag


def test_run_rag_blocks_on_irrelevant_context(
    real_retrieval_item,
):
    """
    If retrieved context is irrelevant,
    run_rag must NOT call the LLM and must
    return answer=None.
    """

    # Force weak similarity
    weak_item = {
        **real_retrieval_item,
        "similarity": 0.12,
        "text": "irrelevant text",
    }

    with patch(
        "pipelines.query.run_rag.retrieve_context_with_scores",
        return_value=[weak_item],
    ), patch(
        "pipelines.query.run_rag.get_llm"
    ) as mock_get_llm:

        result = run_rag("some question")

        # LLM must NEVER be called
        mock_get_llm.assert_not_called()

        assert result.answer is None
        assert result.confidence is not None

        # Confidence semantics (new world)
        assert result.confidence.confidence_level in {"none", "low"}

        # 🔒 STEP 25: IDK must be explainable
        stats = result.confidence.retrieval_stats
        assert stats.get("relevance_gate") == "FAILED"
        assert stats.get("num_chunks") == 1
        assert stats.get("max_similarity") == 0.12


def test_run_rag_calls_llm_on_relevant_context(
    real_retrieval_item,
):
    """
    If context is relevant, run_rag must
    call the LLM exactly once and return an answer.
    """

    strong_item = {
        **real_retrieval_item,
        "similarity": 0.55,
        "text": "relevant text",
    }

    fake_llm = Mock()
    fake_llm.generate.return_value = "grounded answer"

    with patch(
        "pipelines.query.run_rag.retrieve_context_with_scores",
        return_value=[strong_item],
    ), patch(
        "pipelines.query.run_rag.get_llm",
        return_value=fake_llm,
    ) as mock_get_llm:

        result = run_rag("some question")

        # LLM must be called exactly once
        mock_get_llm.assert_called_once()
        fake_llm.generate.assert_called_once()

        assert result.answer == "grounded answer"
        assert result.confidence is not None
        assert result.confidence.confidence_level in {"low", "medium", "high"}
