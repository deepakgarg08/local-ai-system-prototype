# Tests the cross-encoder reranker behavior.
# Ensures that semantically relevant chunks are ranked higher than irrelevant ones.

from pipelines.reranking.cross_encoder import CrossEncoderReranker


def test_reranker_orders_chunks_by_score():
    # Initialize reranker with the production model.
    reranker = CrossEncoderReranker(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    query = "What is machine learning?"

    # Provide one irrelevant and one relevant chunk.
    chunks = [
        {"text": "Bananas are yellow.", "metadata": {}},
        {"text": "Machine learning is a field of artificial intelligence.", "metadata": {}},
    ]

    # Rerank and keep only the top result.
    reranked = reranker.rerank(
        query=query,
        chunks=chunks,
        top_n=1,
    )

    # Verify that the relevant chunk is selected.
    assert len(reranked) == 1
    assert "machine learning" in reranked[0]["text"].lower()
