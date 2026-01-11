from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    safety_flag: str
    is_unsafe: bool
    sources: List[str]
    retrieved_context: Optional[List[str]] = []
    
class LogEntry(BaseModel):
    query: str
    response: str
    safety_flag: str
    is_unsafe: bool
    timestamp: datetime

class FeedbackRequest(BaseModel):
    query: str
    response: str
    feedback: str # "thumbs_up" or "thumbs_down"
