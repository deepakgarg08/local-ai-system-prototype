"""
Tests for metadata-aware ranking.
Ensures metadata boosts influence ordering without overpowering semantic relevance.
"""

from pipelines.retrieval_quality.optimize_ranking import optimize_ranking


def test_metadata_boost_influences_score_but_preserves_relevance():
    chunks = [
        {
            "id": "detail",
            "text": "Termination details ...",
            "score": 0.8,
            "metadata": {"section": "Termination", "page_number": 10},
        },
        {
            "id": "definition",
            "text": "Cancellation means ...",
            "score": 0.75,
            "metadata": {"section": "Definitions", "page_number": 2},
        },
    ]

    ranked = optimize_ranking(
        query="What is cancellation?",
        chunks=chunks,
    )

    # semantic relevance still dominates
    assert ranked[0]["id"] == "detail"

    # but metadata-aware chunk is ranked above its raw-score position
    assert ranked[1]["id"] == "definition"
