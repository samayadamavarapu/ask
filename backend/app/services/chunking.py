from typing import List

class TextChunker:
    """
    Responsible for splitting text into semantic chunks.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """
        Splits text into chunks with overlap.
        Simple sliding window approach. 
        For more complex splitting, one might use sentence boundaries or recursive splitters.
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Move forward by chunk_size - overlap
            # If we reached the end, break
            if end >= text_len:
                break
                
            start += self.chunk_size - self.chunk_overlap
            
        return chunks

    def split_documents(self, documents: List[dict]) -> List[dict]:
        """
        Takes a list of document dicts (content, metadata) and returns chunked documents.
        """
        chunked_docs = []
        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            text_chunks = self.split_text(content)
            
            for i, chunk in enumerate(text_chunks):
                chunked_docs.append({
                    "content": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_index": i
                    }
                })
        return chunked_docs
