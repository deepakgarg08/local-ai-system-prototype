from enum import Enum
from dataclasses import dataclass


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class RetrievalStats:
    top_score: float
    second_score: float | None
    num_chunks: int


def calibrate_confidence(stats: RetrievalStats) -> ConfidenceLevel:
    """
    Determine answer confidence based on retrieval quality.

    Rules are deterministic and explainable.
    """

    # Strong grounding
    if (
        stats.top_score >= 0.80
        and stats.num_chunks >= 2
        and (
            stats.second_score is None
            or (stats.top_score - stats.second_score) >= 0.10
        )
    ):
        return ConfidenceLevel.HIGH

    # Weak grounding
    if stats.top_score < 0.60 or stats.num_chunks == 0:
        return ConfidenceLevel.LOW

    # Everything in between
    return ConfidenceLevel.MEDIUM
