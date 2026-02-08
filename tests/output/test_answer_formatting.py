# tests/output/test_answer_formatting.py

from pipelines.output.format_answer import format_answer


def test_low_confidence_adds_disclaimer():
    formatted = format_answer("some answer", "low")

    assert formatted.answer == "some answer"
    assert formatted.confidence_level == "low"
    assert formatted.disclaimer is not None


def test_medium_confidence_has_no_disclaimer():
    formatted = format_answer("some answer", "medium")

    assert formatted.answer == "some answer"
    assert formatted.confidence_level == "medium"
    assert formatted.disclaimer is None


def test_high_confidence_has_no_disclaimer():
    formatted = format_answer("some answer", "high")

    assert formatted.answer == "some answer"
    assert formatted.confidence_level == "high"
    assert formatted.disclaimer is None


def test_none_confidence_has_no_disclaimer():
    formatted = format_answer("some answer", "none")

    assert formatted.answer == "some answer"
    assert formatted.confidence_level == "none"
    assert formatted.disclaimer is None
