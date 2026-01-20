from pipelines.confidence.calibrate import ConfidenceLevel


def confidence_instruction(confidence: ConfidenceLevel) -> str:
    """
    Returns an instruction string that subtly guides the LLM's tone
    without revealing numeric confidence or allowing self-assessment.
    """

    if confidence == ConfidenceLevel.HIGH:
        return (
            "The retrieved context is strong and unambiguous. "
            "Answer clearly and directly, citing the provided information."
        )

    if confidence == ConfidenceLevel.MEDIUM:
        return (
            "The retrieved context is partially relevant. "
            "Answer carefully and avoid overgeneralization."
        )

    return (
        "The retrieved context is weak or limited. "
        "Do not speculate. If the context is insufficient, say that explicitly."
    )
