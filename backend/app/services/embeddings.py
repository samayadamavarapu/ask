from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import get_settings

settings = get_settings()

class EmbeddingService:
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError

class LocalEmbeddingService(EmbeddingService):
    def __init__(self):
        # Load model once
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

# Factory or Singleton to get the service
_embedding_service = None

def get_embedding_service() -> EmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = LocalEmbeddingService()
    return _embedding_service
