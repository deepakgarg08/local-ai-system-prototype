# tests/analysis/test_step23_safety.py

from analysis.confidence_threshold_calibration import analyze_thresholds


def test_no_threshold_when_answer_idk_overlap():
    events = [
        {"answer_type": "ANSWER", "retrieval_stats": {"min_similarity": 0.15}},
        {"answer_type": "ANSWER", "retrieval_stats": {"min_similarity": 0.18}},
        {"answer_type": "IDK",    "retrieval_stats": {"min_similarity": 0.16}},
        {"answer_type": "IDK",    "retrieval_stats": {"min_similarity": 0.20}},
    ]

    result = analyze_thresholds(events)

    assert result["recommended_thresholds"] == []
