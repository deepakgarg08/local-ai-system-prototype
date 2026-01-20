from pipelines.output.format_answer import format_answer
from pipelines.confidence.calibrate import ConfidenceLevel


def test_low_confidence_adds_disclaimer():
    result = format_answer("Some answer", ConfidenceLevel.LOW)
    assert result.disclaimer is not None


def test_high_confidence_no_disclaimer():
    result = format_answer("Some answer", ConfidenceLevel.HIGH)
    assert result.disclaimer is None
