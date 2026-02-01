# tests/analysis/test_step23_edge_cases.py

from analysis.confidence_threshold_calibration import analyze_thresholds


def test_empty_events_produce_no_threshold():
    result = analyze_thresholds([])

    assert result["total_events"] == 0
    assert result["recommended_thresholds"] == []
