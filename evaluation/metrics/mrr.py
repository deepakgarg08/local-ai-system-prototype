def reciprocal_rank(retrieved: list[str], relevant: list[str]) -> float:
    for idx, r in enumerate(retrieved, start=1):
        if r in relevant:
            return 1.0 / idx
    return 0.0
