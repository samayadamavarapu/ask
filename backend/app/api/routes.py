from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.api.schemas import QueryRequest, QueryResponse, LogEntry, FeedbackRequest
from app.services.safety import get_safety_guard
from app.services.retrieval import get_retrieval_service
from app.services.generation import get_generation_service
from app.db.mongo import db
from typing import List
import json

router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest, background_tasks: BackgroundTasks):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # 1. Safety Check
    safety_guard = get_safety_guard()
    is_unsafe, safety_flag, safety_msg = safety_guard.check_query(query)

    retrieved_chunks = []
    sources = []
    answer = ""

    if safety_flag == "BLOCKED":
        answer = safety_msg
    elif is_unsafe:
         # For UNSAFE but not BLOCKED, we still want to give the safety message 
         # but potentially retrieval logic is skipped or limited. 
         # The requirement says: Return a response that contains a gentle safety message, modification, etc.
         answer = safety_msg
    else:
        # 2. Retrieval
        retrieval_service = get_retrieval_service()
        retrieval_results = retrieval_service.retrieve(query)
        
        # Extract content for generation and sources for display
        retrieved_chunks = [res["content"] for res in retrieval_results]
        
        # Parse metadata for sources
        for res in retrieval_results:
            meta = res.get("metadata", {})
            # Try to get title from original_data JSON string if possible
            title = meta.get("source", "Unknown Source")
            try:
                if "original_data" in meta:
                    orig = json.loads(meta["original_data"])
                    if "title" in orig:
                        title = orig["title"]
            except:
                pass
            sources.append(title)
        
        # 3. Generation
        generation_service = get_generation_service()
        raw_answer = generation_service.generate_response(query, retrieved_chunks, safety_flag)
        
        # 4. Soften Response if needed (SafetyGuard handles most logic now, but keep as fallback)
        answer = raw_answer

    # 5. Logging (Background Task to not block response)
    background_tasks.add_task(
        db.log_interaction,
        query=query,
        response=answer,
        retrieved_chunks=retrieved_chunks,
        safety_flag=safety_flag,
        is_unsafe=is_unsafe
    )

    return QueryResponse(
        answer=answer,
        safety_flag=safety_flag,
        is_unsafe=is_unsafe,
        sources=sources,
        retrieved_context=retrieved_chunks
    )

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    if db.db is None:
        return {"status": "error", "message": "Database not connected"}
    
    await db.db.feedback.insert_one(request.dict())
    return {"status": "success", "message": "Feedback received"}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Yoga RAG API"}

@router.get("/logs", response_model=List[LogEntry])
async def get_logs(limit: int = 10):
    if db.db is None:
        return []
    
    try:
        cursor = db.db.interactions.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
        logs = await cursor.to_list(length=limit)
        return logs
    except Exception as e:
        # In production, log this error properly
        print(f"Error fetching logs: {e}")
        return []
