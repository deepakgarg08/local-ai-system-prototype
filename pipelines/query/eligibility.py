# pipelines/query/eligibility.py

from configs.retrieval import CORPUS_PROFILE, MIN_CONTEXT_RULES

def is_answer_eligible(chunks: list[dict]) -> bool:
    rules = MIN_CONTEXT_RULES[CORPUS_PROFILE]

    high = [c for c in chunks if c["relevance"] == "high"]
    medium = [c for c in chunks if c["relevance"] == "medium"]

    if high:
        tokens = sum(len(c["text"].split()) for c in high)
        return (
            len(high) >= rules["high"]["min_chunks"]
            and tokens >= rules["high"]["min_tokens"]
        )

    if medium:
        tokens = sum(len(c["text"].split()) for c in medium)
        return (
            len(medium) >= rules["medium"]["min_chunks"]
            and tokens >= rules["medium"]["min_tokens"]
        )

    return False
