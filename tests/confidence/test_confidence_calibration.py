# tests/confidence/test_confidence_calibration.py

from pipelines.confidence.calibrate import (
    RetrievalStats,
    recommend_confidence_thresholds,
)


def test_recommend_confidence_thresholds_produces_recommendations():
    """
    STEP 26:
    Calibration must recommend thresholds based on historical behavior,
    not classify individual retrievals.
    """

    historical_stats = [
        RetrievalStats(
            top_score=0.85,
            second_score=0.70,
            num_chunks=3,
            answer_type="ANSWER",
        ),
        RetrievalStats(
            top_score=0.68,
            second_score=0.64,
            num_chunks=1,
            answer_type="ANSWER",
        ),
        RetrievalStats(
            top_score=0.45,
            second_score=0.40,
            num_chunks=2,
            answer_type="IDK",
        ),
        RetrievalStats(
            top_score=0.90,
            second_score=None,
            num_chunks=0,
            answer_type="IDK",
        ),
    ]

    thresholds = recommend_confidence_thresholds(historical_stats)

    # Structural guarantees
    assert thresholds.high_min_top_score >= 0.0
    assert thresholds.low_max_top_score >= 0.0
    assert thresholds.high_min_chunks == 2
    assert thresholds.high_min_score_gap == 0.10

    # Human-reviewable explanation must exist
    assert isinstance(thresholds.notes, list)
    assert len(thresholds.notes) > 0
