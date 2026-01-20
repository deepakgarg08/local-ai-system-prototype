from pipelines.confidence.calibrate import (
    calibrate_confidence,
    RetrievalStats,
    ConfidenceLevel,
)


def test_high_confidence_when_strong_retrieval():
    stats = RetrievalStats(
        top_score=0.85,
        second_score=0.70,
        num_chunks=3,
    )

    assert calibrate_confidence(stats) == ConfidenceLevel.HIGH


def test_low_confidence_when_weak_score():
    stats = RetrievalStats(
        top_score=0.45,
        second_score=0.40,
        num_chunks=2,
    )

    assert calibrate_confidence(stats) == ConfidenceLevel.LOW


def test_low_confidence_when_no_chunks():
    stats = RetrievalStats(
        top_score=0.90,
        second_score=None,
        num_chunks=0,
    )

    assert calibrate_confidence(stats) == ConfidenceLevel.LOW


def test_medium_confidence_in_ambiguous_case():
    stats = RetrievalStats(
        top_score=0.68,
        second_score=0.64,
        num_chunks=1,
    )

    assert calibrate_confidence(stats) == ConfidenceLevel.MEDIUM
