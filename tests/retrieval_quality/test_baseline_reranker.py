"""
Ensures the baseline reranker preserves retrieval order.
This test protects STEP 20 control behavior from accidental regression.
"""

from pipelines.retrieval_quality.optimize_ranking import optimize_ranking


def test_baseline_reranker_preserves_order():
    chunks = [
        {"id": "a", "text": "first"},
        {"id": "b", "text": "second"},
        {"id": "c", "text": "third"},
    ]

    ranked = optimize_ranking(
        query="irrelevant query",
        chunks=chunks,
    )

    assert ranked == chunks
