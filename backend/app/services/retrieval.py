from typing import List, Dict, Any
from app.services.vector_store import get_vector_db
from app.core.config import get_settings

settings = get_settings()

class RetrievalService:
    def __init__(self):
        self.vector_db = get_vector_db()

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieves top-k relevant chunks for the query.
        Returns a list of dicts with 'content', 'metadata', 'score'.
        """
        results = self.vector_db.search(query, k=settings.TOP_K_RETRIEVAL)
        return results

_retrieval_service = None
def get_retrieval_service() -> RetrievalService:
    global _retrieval_service
    if _retrieval_service is None:
        _retrieval_service = RetrievalService()
    return _retrieval_service
