from dataclasses import dataclass
from pipelines.confidence.calibrate import ConfidenceLevel


@dataclass(frozen=True)
class FormattedAnswer:
    answer: str
    confidence: ConfidenceLevel
    disclaimer: str | None = None


def format_answer(
    answer: str,
    confidence: ConfidenceLevel,
) -> FormattedAnswer:
    """
    Attach confidence metadata for UI or API layers.
    """

    disclaimer = None

    if confidence == ConfidenceLevel.LOW:
        disclaimer = (
            "⚠️ The available documents do not provide strong support "
            "for a definitive answer. Please verify manually."
        )

    return FormattedAnswer(
        answer=answer,
        confidence=confidence,
        disclaimer=disclaimer,
    )
