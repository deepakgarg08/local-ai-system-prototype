"""
Applies deterministic score boosts based on chunk metadata.

This module improves ranking quality by prioritizing chunks that are
structurally more important (e.g. definitions, key sections, newer docs),
without affecting correctness or filtering.
"""

from typing import Dict


def compute_metadata_boost(chunk: Dict) -> float:
    """
    Compute a metadata-based boost score for a chunk.

    This function must:
    - be deterministic
    - be explainable
    - never return negative values
    """

    boost = 0.0
    metadata = chunk.get("metadata", {})

    section = metadata.get("section", "").lower()
    if "definition" in section:
        boost += 0.2
    if "termination" in section or "cancellation" in section:
        boost += 0.3

    document_type = metadata.get("document_type", "").lower()
    if document_type in {"contract", "policy", "specification"}:
        boost += 0.1

    page_number = metadata.get("page_number")
    if isinstance(page_number, int) and page_number <= 3:
        boost += 0.1

    return boost
