# Defines the abstract contract for answer gating.
# Gates decide whether an LLM is allowed to generate an answer.

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseGate(ABC):
    @abstractmethod
    def allow_answer(self, chunks: List[Dict]) -> bool:
        """
        Return True if an answer is allowed, False otherwise.
        """
        raise NotImplementedError
