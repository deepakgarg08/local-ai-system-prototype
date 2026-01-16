from typing import List, Dict


def apply_retrieval_strategy(
    chunks: List[Dict],
    top_k: int = 6,
    score_threshold: float = 0.25,
) -> List[Dict]:
    """
    Apply retrieval filtering and ordering.

    Args:
        chunks: raw vector search output (must include 'score')
        top_k: max number of chunks to keep
        score_threshold: minimum similarity score

    Returns:
        filtered and ordered chunks
    """

    # 1. Drop low-quality chunks
    filtered = [
        ch for ch in chunks
        if ch.get("score", 0.0) >= score_threshold
    ]

    # 2. Sort by score (descending)
    filtered.sort(key=lambda x: x["score"], reverse=True)

    # 3. Keep only top_k
    return filtered[:top_k]


# Example usage, can be removed in production

if __name__ == "__main__":
    dummy_chunks = [
        {"text": "A", "score": 0.91},
        {"text": "B", "score": 0.40},
        {"text": "C", "score": 0.10},
    ]

    result = apply_retrieval_strategy(
        dummy_chunks,
        top_k=2,
        score_threshold=0.3,
    )

    for ch in result:
        print(ch)
