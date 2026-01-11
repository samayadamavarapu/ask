import sys
import os
import glob

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ingestion import KnowledgeIngestion
from app.services.chunking import TextChunker
from app.services.vector_store import get_vector_db

def ingest_data(data_dir: str):
    print(f"Scanning {data_dir} for documents...")
    files = glob.glob(os.path.join(data_dir, "**/*.*"), recursive=True)
    
    if not files:
        print("No files found.")
        return

    vector_db = get_vector_db()
    chunker = TextChunker()
    
    total_chunks = 0
    
    for file_path in files:
        if not file_path.lower().endswith(('.json', '.txt', '.pdf', '.md')):
            continue
            
        print(f"Processing {file_path}...")
        try:
            # 1. Load
            docs = KnowledgeIngestion.load_file(file_path)
            
            # 2. Chunk
            chunked_docs = chunker.split_documents(docs)
            
            # 3. Store
            if chunked_docs:
                vector_db.add_documents(chunked_docs)
                total_chunks += len(chunked_docs)
                print(f"  -> Added {len(chunked_docs)} chunks.")
            else:
                print("  -> No content extracted.")
                
        except Exception as e:
            print(f"  -> Error: {e}")

    print(f"\nIngestion Complete! Total chunks stored: {total_chunks}")

if __name__ == "__main__":
    data_directory = "data/knowledge_base"
    if len(sys.argv) > 1:
        data_directory = sys.argv[1]
    
    ingest_data(data_directory)
