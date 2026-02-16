from sentence_transformers import SentenceTransformer
from configs.embeddings import EMBEDDING_MODEL_NAME

class Embedder:
    
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
