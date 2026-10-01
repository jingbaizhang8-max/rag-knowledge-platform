from fastapi import APIRouter

from app.schemas.ask import AskResponse,AskRequest
from app.services.rag_service import ask_question

router = APIRouter()

@router.post("", response_model=AskResponse)
def ask(request: AskRequest):
    result = ask_question(
        query=request.query,
        limit=request.limit,
        document_id=request.document_id
    )

    return {
        "query": request.query,
        "answer": result["answer"],
        "sources": result["sources"]
    }