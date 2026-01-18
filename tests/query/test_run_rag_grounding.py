import pytest
from unittest.mock import Mock, patch

from pipelines.query.run_rag import run_rag


def test_run_rag_blocks_on_irrelevant_context():
    """
    If retrieved context is irrelevant,
    run_rag must NOT call the LLM and must
    return a deterministic 'I don't know'.
    """

    with patch(
        "pipelines.query.run_rag.retrieve_context_with_scores"
    ) as mock_retrieve, patch(
        "pipelines.query.run_rag.get_llm"
    ) as mock_get_llm:

        # Retrieval returns weak similarity
        mock_retrieve.return_value = [
            ("irrelevant text", 0.12),
            ("still irrelevant", 0.18),
        ]

        result = run_rag("some question")

        # LLM must NEVER be called
        mock_get_llm.assert_not_called()

        assert "I don't know" in result


def test_run_rag_calls_llm_on_relevant_context():
    """
    If context is relevant, run_rag must
    call the LLM exactly once.
    """

    with patch(
        "pipelines.query.run_rag.retrieve_context_with_scores"
    ) as mock_retrieve, patch(
        "pipelines.query.run_rag.get_llm"
    ) as mock_get_llm:

        mock_retrieve.return_value = [
            ("relevant text", 0.55),
        ]

        # Mock LLM
        fake_llm = Mock()
        fake_llm.generate.return_value = "grounded answer"
        mock_get_llm.return_value = fake_llm

        result = run_rag("some question")

        mock_get_llm.assert_called_once()
        fake_llm.generate.assert_called_once()

        assert result == "grounded answer"
