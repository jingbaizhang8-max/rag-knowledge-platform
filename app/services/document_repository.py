from sqlalchemy.orm import Session

from app.models.document import Document
from sqlalchemy import select
def create_document_record(
        db: Session,
        document_id: str,
        filename: str,
        page_count: int,
        chunk_count: int,
        status: str
) -> Document:

    document = Document(
        document_id=document_id,
        filename=filename,
        page_count=page_count,
        chunk_count=chunk_count,
        status=status
    )
    try:
        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    except Exception:
        db.rollback()
        raise


def list_document_records(db):
    statement = (
        select(Document).order_by(Document.created_at.desc())
    )

    return  db.scalars(statement).all()