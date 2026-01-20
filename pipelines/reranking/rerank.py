# Provides a simple orchestration function for reranking.
# Keeps model selection and policy logic out of retrieval and prompting layers.

from typing import List, Dict

from pipelines.reranking.cross_encoder import CrossEncoderReranker


def rerank_chunks(
    query: str,
    chunks: List[Dict],
    top_n: int,
) -> List[Dict]:
    # Instantiate the reranker with a strong default model.
    reranker = CrossEncoderReranker(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    # Rerank retrieved chunks and return the top-N results.
    return reranker.rerank(
        query=query,
        chunks=chunks,
        top_n=top_n,
    )
