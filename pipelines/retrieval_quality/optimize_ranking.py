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
