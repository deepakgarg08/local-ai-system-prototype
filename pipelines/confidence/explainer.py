from .models import ConfidenceReport, RetrievalEvidence

def build_explanation(
    confidence: ConfidenceReport,
    evidence: list[RetrievalEvidence]
) -> str:
    if confidence.confidence_level == "none":
        return (
            "No sufficiently relevant internal information was found. "
            "The system did not generate an answer."
        )

    sources = {e.source_document for e in evidence}

    return (
        f"Confidence level: {confidence.confidence_level.upper()}. "
        f"The answer is based on {len(evidence)} retrieved text sections "
        f"from {len(sources)} internal document(s). "
        "Please verify the result before using it operationally."
    )
