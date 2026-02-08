# tests/prompting/test_confidence_prompt.py

from pipelines.prompting.confidence_prompt import confidence_instruction


def test_low_confidence_instruction():
    text = confidence_instruction("low")
    assert "weakly supported" in text.lower()


def test_medium_confidence_instruction():
    text = confidence_instruction("medium")
    assert "moderately supported" in text.lower()


def test_high_confidence_instruction():
    text = confidence_instruction("high")
    assert "well supported" in text.lower()


def test_none_confidence_instruction():
    text = confidence_instruction("none")
    assert "no sufficient information" in text.lower()
