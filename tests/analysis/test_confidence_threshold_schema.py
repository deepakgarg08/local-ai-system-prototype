# tests/analysis/test_step23_schema.py

from analysis.confidence_threshold_calibration import analyze_thresholds


def test_confidence_threshold_schema():
    result = analyze_thresholds([])

    assert isinstance(result, dict)
    assert "total_events" in result
    assert "answered" in result
    assert "idk" in result
    assert "candidate_thresholds" in result
    assert "recommended_thresholds" in result
