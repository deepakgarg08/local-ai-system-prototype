# pipelines/prompting/confidence_prompt.py

from typing import Literal


def confidence_instruction(
    confidence_level: Literal["high", "medium", "low", "none"]
) -> str:
    if confidence_level == "low":
        return (
            "The following answer may be weakly supported. "
            "Avoid speculation and prefer extractive phrasing."
        )

    if confidence_level == "medium":
        return (
            "The following answer is moderately supported "
            "by the available documents."
        )

    if confidence_level == "high":
        return (
            "The following answer is well supported "
            "by the available documents."
        )

    # "none" → IDK
    return (
        "No sufficient information is available to answer the question."
    )
