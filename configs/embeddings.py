"""
Embedding configuration
Single source of truth for embedding model.
"""

# This model was trained for:
# Short sentence similarity
# Semantic textual similarity tasks
# Not long-form scientific documents

# EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# These are: BAAI/bge-base-en-v1.5
# Designed for retrieval
# Strong on academic corpora
# Much better semantic alignment
# Produce 768-dim vectors

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"
# EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"
