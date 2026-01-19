# pipelines/retrieval_quality/rerankers/base.py

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseReranker(ABC):
    @abstractmethod
    def rerank(
        self,
        query: str,
        chunks: List[Dict],
    ) -> List[Dict]:
        """
        Reorder chunks based on relevance to the query.

        Must:
        - NOT remove chunks
        - NOT add chunks
        - ONLY change ordering
        """
        raise NotImplementedError
