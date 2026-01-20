# Implements score-based answer gating.
# Blocks LLM calls when reranked evidence is too weak.

from typing import List, Dict

from pipelines.gating.base import BaseGate


class ScoreThresholdGate(BaseGate):
    def __init__(self, min_score: float):
        self.min_score = min_score

    def allow_answer(self, chunks: List[Dict]) -> bool:
        if not chunks:
            return False

        best_score = max(
            chunk.get("rerank_score", 0.0) for chunk in chunks
        )

        return best_score >= self.min_score
