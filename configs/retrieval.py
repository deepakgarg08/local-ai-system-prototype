# configs/retrieval.py

# Corpus maturity profile
# Controls how strict retrieval gating should be
CORPUS_PROFILE = "small"  
# allowed: "small" | "growing" | "mature"

SIMILARITY_THRESHOLDS = {
    "high": 0.78,
    "medium": 0.62,
    "low": 0.50,
}

# Adaptive thresholds
MIN_CONTEXT_RULES = {
    "high": {
        "min_chunks": 1,
        "min_tokens": 40
    },
    "medium": {
        "min_chunks": 2,
        "min_tokens": 80
    }
}

MAX_CHUNKS_AFTER_FILTER = 6
