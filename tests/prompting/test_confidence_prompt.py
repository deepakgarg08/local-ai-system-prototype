from pipelines.prompting.confidence_prompt import confidence_instruction
from pipelines.confidence.calibrate import ConfidenceLevel


def test_high_confidence_instruction():
    text = confidence_instruction(ConfidenceLevel.HIGH)
    assert "strong and unambiguous" in text


def test_medium_confidence_instruction():
    text = confidence_instruction(ConfidenceLevel.MEDIUM)
    assert "partially relevant" in text


def test_low_confidence_instruction():
    text = confidence_instruction(ConfidenceLevel.LOW)
    assert "Do not speculate" in text
