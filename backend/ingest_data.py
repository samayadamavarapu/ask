import sys
import os

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.services.vector_store import get_vector_db
from app.services.ingestion import KnowledgeIngestion

def ingest():
    print("Starting ingestion...")
    # Adjust path based on where we run the script from
    # Assuming running from 'backend' directory
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base", "yoga_knowledge_base.json"))
    
    print(f"Loading data from {file_path}")
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    docs = KnowledgeIngestion.load_file(file_path)
    print(f"Loaded {len(docs)} documents.")
    
    vector_db = get_vector_db()
    # ChromaDB might complain if IDs are duplicates, but our ID generation uses hash of content, so it should be idempotent-ish.
    # However, to be clean, we might want to reset, but for now appending is safer than deleting everything.
    print("Adding to vector store...")
    vector_db.add_documents(docs)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest()
