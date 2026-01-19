# pipelines/retrieval_quality/rerankers/baseline_reranker.py
"""
Baseline reranker used as a control.
Preserves the original retrieval order without applying any ranking logic.
"""

from typing import List, Dict
from .base import BaseReranker


class BaselineReranker(BaseReranker):
    def rerank(
        self,
        query: str,
        chunks: List[Dict],
    ) -> List[Dict]:
        return chunks
