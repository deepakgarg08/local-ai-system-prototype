# Implements a neural cross-encoder reranker using sentence-transformers.
# Computes true relevance scores by jointly encoding (query, chunk) pairs.

from typing import List, Dict
from sentence_transformers import CrossEncoder

from pipelines.reranking.base import BaseReranker


class CrossEncoderReranker(BaseReranker):
    def __init__(self, model_name: str):
        # Loads the cross-encoder model once for reuse across queries.
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        chunks: List[Dict],
        top_n: int,
    ) -> List[Dict]:
        # Returns early if no chunks are provided.
        if not chunks:
            return []

        # Build query–chunk pairs for joint encoding.
        pairs = [(query, chunk["text"]) for chunk in chunks]

        # Predict relevance scores for each pair.
        scores = self.model.predict(pairs)

        # Attach rerank scores to each chunk.
        for chunk, score in zip(chunks, scores):
            chunk["rerank_score"] = float(score)

        # Sort chunks by descending relevance score.
        reranked = sorted(
            chunks,
            key=lambda c: c["rerank_score"],
            reverse=True,
        )

        # Return only the top-N most relevant chunks.
        return reranked[:top_n]
