import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
from app.core.config import get_settings
from app.services.embeddings import get_embedding_service

settings = get_settings()

class VectorDB:
    def __init__(self):
        # Persistent Client
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
        self.embedding_service = get_embedding_service()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="yoga_knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Embeds and stores documents.
        documents: List of dicts with 'content' and 'metadata'.
        """
        if not documents:
            return

        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        ids = [f"id_{i}_{hash(text)}" for i, text in enumerate(texts)] # Simple ID generation
        
        # Generate embeddings
        embeddings = self.embedding_service.generate_embeddings(texts)
        
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Semantic search.
        """
        query_embedding = self.embedding_service.generate_embeddings([query])[0]
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # Format results
        # Chroma returns lists of lists
        formatted_results = []
        if results["documents"]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": results["distances"][0][i] if results["distances"] else 0.0
                })
                
        return formatted_results

# Singleton
_vector_db = None

def get_vector_db() -> VectorDB:
    global _vector_db
    if _vector_db is None:
        _vector_db = VectorDB()
    return _vector_db
