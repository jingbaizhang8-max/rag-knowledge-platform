from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.query_history_repository import create_query_history

from app.schemas.ask import AskResponse,AskRequest
from app.services.rag_service import ask_question

from app.core.logger import logger

router = APIRouter()

@router.post("", response_model=AskResponse)
def ask(
        request: AskRequest,
        db: Session = Depends(get_db)
        ):

    logger.info(
        "Ask request received | document_id=%s | limit=%s",
        request.document_id,
        request.limit
    )

    try:
        result = ask_question(
            query=request.query,
            limit=request.limit,
            document_id=request.document_id
        )

        create_query_history(
            db=db,
            query=request.query,
            answer=result["answer"],
            document_id=request.document_id,
            sources=result["sources"]
        )

        logger.info(
            "Ask completed | sources=%s",
            len(result["sources"])
        )

        return {
            "query": request.query,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception:
        logger.exception(
            "Ask request failed | document_id=%s",
            request.document_id
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process question."
        )