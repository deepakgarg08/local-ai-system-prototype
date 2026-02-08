from typing import List, Tuple

# -----------------------------
# Relevance Policy (v0.2)
# -----------------------------

# Conservative default.
# With MiniLM embeddings, cosine similarity above ~0.30
# usually indicates semantic overlap.
from configs.loader import load_active_config

config = load_active_config()
MIN_SIMILARITY_THRESHOLD = config["retrieval"]["min_similarity_threshold"]
print(f"Using MIN_SIMILARITY_THRESHOLD pipelines/query/relevance.py: {MIN_SIMILARITY_THRESHOLD}")

def is_context_relevant(
    retrieved_chunks: List[Tuple[str, float]]
) -> bool:
    """
    Decide whether retrieved context is relevant enough
    to allow LLM invocation.

    Rule (simple & deterministic):
    - At least ONE chunk must exceed the threshold
    """

    scores = [
            item.get("similarity")
            for item in retrieved_chunks
            if isinstance(item, dict)
        ]

    if not scores:
        return False

    return max(scores) >= MIN_SIMILARITY_THRESHOLD
