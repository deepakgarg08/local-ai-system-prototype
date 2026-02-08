# pipelines/confidence/calibrate.py

"""
STEP 26 — Offline Confidence Calibration

This module performs OFFLINE analysis of historical retrieval statistics
and produces RECOMMENDED confidence thresholds.

IMPORTANT GUARANTEES:
- This module MUST NOT be imported by runtime query pipelines.
- This module NEVER classifies individual queries.
- This module NEVER modifies live configuration automatically.
- All outputs require explicit human review before application.

The purpose of this module is to support evidence-based tuning
while preserving determinism, safety, and human authority.
"""

from dataclasses import dataclass
from typing import Iterable


# ---------------------------------------------------------------------
# Input data model (derived from telemetry)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RetrievalStats:
    """
    Aggregated retrieval characteristics observed at runtime.

    These values are collected from telemetry logs and represent
    historical system behavior, not live query inputs.
    """
    top_score: float
    second_score: float | None
    num_chunks: int
    answer_type: str  # "ANSWER" or "IDK"


# ---------------------------------------------------------------------
# Output data model (calibration artifact)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RecommendedConfidenceThresholds:
    """
    Recommended thresholds for runtime confidence scoring.

    These values are NOT applied automatically.
    They must be reviewed and manually copied into configuration.
    """
    high_min_top_score: float
    high_min_chunks: int
    high_min_score_gap: float
    low_max_top_score: float

    notes: list[str]


# ---------------------------------------------------------------------
# Calibration logic (offline only)
# ---------------------------------------------------------------------

def recommend_confidence_thresholds(
    historical_stats: Iterable[RetrievalStats],
) -> RecommendedConfidenceThresholds:
    """
    Analyze historical retrieval statistics and recommend
    confidence classification thresholds.

    This function:
    - does NOT classify queries
    - does NOT enforce behavior
    - only observes patterns in past executions
    """

    answer_scores: list[float] = []
    idk_scores: list[float] = []

    for stat in historical_stats:
        if stat.answer_type == "ANSWER":
            answer_scores.append(stat.top_score)
        elif stat.answer_type == "IDK":
            idk_scores.append(stat.top_score)

    # Defensive defaults (in case of sparse data)
    if not answer_scores:
        answer_scores = [0.8]
    if not idk_scores:
        idk_scores = [0.6]

    # Simple, explainable heuristics
    high_min_top_score = round(min(answer_scores), 2)
    low_max_top_score = round(max(idk_scores), 2)

    notes: list[str] = [
        f"Observed {len(answer_scores)} answered queries and {len(idk_scores)} IDK cases.",
        f"Answers typically occur at similarity ≥ {high_min_top_score}.",
        f"IDK cases cluster at similarity ≤ {low_max_top_score}.",
        "Thresholds are recommendations and require human review.",
    ]

    return RecommendedConfidenceThresholds(
        high_min_top_score=high_min_top_score,
        high_min_chunks=2,
        high_min_score_gap=0.10,
        low_max_top_score=low_max_top_score,
        notes=notes,
    )


# ---------------------------------------------------------------------
# Optional: human-readable calibration summary
# ---------------------------------------------------------------------

def format_calibration_report(
    thresholds: RecommendedConfidenceThresholds,
) -> str:
    """
    Render a human-readable calibration report.
    Intended for Markdown / console output.
    """

    return (
        "STEP 26 — Offline Confidence Calibration Report\n\n"
        f"- Recommended HIGH confidence minimum similarity: {thresholds.high_min_top_score}\n"
        f"- Recommended minimum chunks for HIGH confidence: {thresholds.high_min_chunks}\n"
        f"- Recommended minimum score gap for HIGH confidence: {thresholds.high_min_score_gap}\n"
        f"- Recommended LOW confidence ceiling similarity: {thresholds.low_max_top_score}\n\n"
        "Notes:\n"
        + "\n".join(f"- {note}" for note in thresholds.notes)
        + "\n\n"
        "⚠ These values are NOT applied automatically.\n"
        "⚠ Human review and explicit configuration changes are required."
    )
