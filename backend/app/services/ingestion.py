import json
import os
from typing import List, Dict, Any
from pypdf import PdfReader

class KnowledgeIngestion:
    """
    Handles loading and normalizing data from various file formats.
    """
    
    @staticmethod
    def load_file(file_path: str) -> List[Dict[str, Any]]:
        """
        Loads a file and returns a list of documents (usually one per file, or multiple for JSON).
        Each document is a dict: {"content": str, "metadata": dict}
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".json":
            return KnowledgeIngestion._load_json(file_path)
        elif ext == ".pdf":
            return KnowledgeIngestion._load_pdf(file_path)
        elif ext in [".txt", ".md"]:
            return KnowledgeIngestion._load_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _load_json(file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Expecting JSON to be a list of objects or a single object
        # We need to standardize to {"content": "...", "metadata": ...}
        # If the JSON structure is specific (e.g. Q&A pairs), we map it here.
        # For this generic implementation, we assume a flexible structure.
        
        docs = []
        if isinstance(data, list):
            for item in data:
                content = json.dumps(item) # Fallback if no specific content field
                if "content" in item:
                    content = item["content"]
                elif "text" in item:
                    content = item["text"]
                elif "question" in item and "answer" in item:
                    content = f"Question: {item['question']}\nAnswer: {item['answer']}"
                
                docs.append({
                    "content": content,
                    "metadata": {"source": os.path.basename(file_path), "original_data": json.dumps(item)}
                })
        elif isinstance(data, dict):
             # Similar logic for single dict
             content = json.dumps(data)
             docs.append({
                 "content": content,
                 "metadata": {"source": os.path.basename(file_path)}
             })
             
        return docs

    @staticmethod
    def _load_pdf(file_path: str) -> List[Dict[str, Any]]:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Normalize whitespace
        text = " ".join(text.split())
        
        return [{
            "content": text,
            "metadata": {"source": os.path.basename(file_path)}
        }]

    @staticmethod
    def _load_text(file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        return [{
            "content": text,
            "metadata": {"source": os.path.basename(file_path)}
        }]
