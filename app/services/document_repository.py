from sqlalchemy.orm import Session

from app.models.document import Document

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