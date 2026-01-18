def precision_at_k(retrieved: list[str], relevant: list[str], k: int) -> float:
    retrieved_k = retrieved[:k]
    if not retrieved_k:
        return 0.0
    hits = sum(1 for r in retrieved_k if r in relevant)
    return hits / len(retrieved_k)
