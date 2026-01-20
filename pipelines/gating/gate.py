from pipelines.confidence.models import ConfidenceReport


def is_answer_allowed(
    *,
    answer: str,
    confidence: ConfidenceReport,
    extractive_only: bool,
) -> bool:
    """
    Post-generation answer gate.

    This gate decides whether a generated answer may be returned,
    based strictly on already-computed confidence signals.

    It MUST:
    - be deterministic
    - not contradict retrieval grounding
    - not invent new confidence semantics
    """

    # 1. Empty or whitespace-only answers are never allowed
    if not answer or not answer.strip():
        return False

    # 2. Extractive-only mode is the safest possible case
    #    If we forced extractive answers, they are always allowed
    if extractive_only:
        return True

    # 3. Interpret semantic confidence levels
    #
    # Allowed:
    #   - high
    #   - medium
    #
    # Blocked:
    #   - low
    #   - none
    if confidence.confidence_level in ("low", "none"):
        return False

    # 4. Otherwise, allow the answer
    return True
