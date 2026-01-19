# pipelines/retrieval_quality/optimize_ranking.py
"""
STEP 20 entry point.
Applies ranking optimizations to retrieved chunks without affecting correctness.
"""

from typing import List, Dict
from pipelines.retrieval_quality.rerankers.baseline_reranker import (
    BaselineReranker,
)


def optimize_ranking(
    query: str,
    chunks: List[Dict],
) -> List[Dict]:
    reranker = BaselineReranker()
    return reranker.rerank(query=query, chunks=chunks)
"""
STEP 20 entry point.

Combines baseline ranking with deterministic metadata-based boosts.
This module improves ranking quality without changing correctness,
filtering, or safety behavior.
"""

from typing import List, Dict

from pipelines.retrieval_quality.rerankers.baseline_reranker import (
    BaselineReranker,
)
from pipelines.retrieval_quality.scoring.metadata_boost import (
    compute_metadata_boost,
)


def optimize_ranking(
    query: str,
    chunks: List[Dict],
) -> List[Dict]:
    """
    Optimize ranking of retrieved chunks using metadata signals.

    This function:
    - preserves all chunks
    - reorders chunks only
    - remains deterministic and explainable
    """

    reranker = BaselineReranker()
    ranked = reranker.rerank(query=query, chunks=chunks)

    def score(chunk: Dict) -> float:
        base_score = chunk.get("score", 0.0)
        metadata_boost = compute_metadata_boost(chunk)
        return base_score + metadata_boost

    return sorted(ranked, key=score, reverse=True)
