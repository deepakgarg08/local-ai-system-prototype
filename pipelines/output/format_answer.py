# pipelines/output/format_answer.py

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class FormattedAnswer:
    answer: str
    confidence_level: Literal["high", "medium", "low", "none"]
    disclaimer: str | None = None


def format_answer(
    answer: str,
    confidence_level: Literal["high", "medium", "low", "none"],
) -> FormattedAnswer:
    """
    Attach confidence metadata for UI or API layers.

    This function is presentation-only and must not
    introduce policy or decision logic.
    """

    disclaimer = None

    if confidence_level == "low":
        disclaimer = (
            "⚠️ The available documents do not provide strong support "
            "for a definitive answer. Please verify manually."
        )

    return FormattedAnswer(
        answer=answer,
        confidence_level=confidence_level,
        disclaimer=disclaimer,
    )
