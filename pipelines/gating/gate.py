# Orchestrates answer gating policies.
# Keeps threshold configuration out of core logic.

from typing import List, Dict

from pipelines.gating.score_gate import ScoreThresholdGate
from configs.runtime import RERANK_MIN_SCORE

def is_answer_allowed(chunks: List[Dict]) -> bool:
    gate = ScoreThresholdGate(min_score=RERANK_MIN_SCORE) # Example threshold, Threshold is explicit, testable, and easy to tune.

    return gate.allow_answer(chunks)
