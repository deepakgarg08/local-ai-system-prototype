# Defines the abstract contract for all rerankers.
# Ensures different reranking strategies can be swapped without changing callers.

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseReranker(ABC):
    @abstractmethod
    def rerank(
        self,
        query: str,
        chunks: List[Dict],
        top_n: int,
    ) -> List[Dict]:
        """
        Rerank retrieved chunks by relevance to the query.

        Expected chunk fields:
        - text: str
        - metadata: dict
        - optional retrieval score
        """
        raise NotImplementedError
