from sqlalchemy.orm import Session

from app.models.query_history import QueryHistory


def create_query_history(
    db: Session,
    query: str,
    answer: str,
    document_id: str | None,
    sources: list[dict]
) -> QueryHistory:

    history = QueryHistory(
        query=query,
        answer=answer,
        document_id=document_id,
        sources=sources
    )
    try:
        db.add(history)
        db.commit()
        db.refresh(history)


        return history

    except Exception:
        db.rollback()
        raise