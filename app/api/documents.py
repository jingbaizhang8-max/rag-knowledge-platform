
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
from uuid import uuid4
from app.services.ingestion_service import ingest_document

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.document_repository import create_document_record
from app.core.logger import logger

router = APIRouter()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


@router.post("/upload")
async def upload_document(
        file: UploadFile=File(...),
        db: Session = Depends(get_db)
):
    original_filename = file.filename or "unknown"
    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT and Markdown files are supported."
        )
    document_id = str(uuid4())
    saved_filename=f"{document_id}{extension}"
    file_path=UPLOAD_DIR / saved_filename

    logger.info(
        "Document upload started | filename=%s | document_id=%s",
        original_filename,
        document_id
    )

    try:

        content = await file.read()
        with open(file_path, "wb") as saved_file:
            saved_file.write(content)

        ingestion_result = ingest_document(
            file_path = file_path,
            document_id=document_id,
            source=original_filename
        )

        create_document_record(
            db=db,
            document_id=document_id,
            filename=original_filename,
            page_count=ingestion_result["page_count"],
            chunk_count=ingestion_result["chunk_count"],
            status="indexed"
        )

        return {
            "document_id": document_id,
            "filename": original_filename,
            "content_type": file.content_type,
            "size": len(content),
            "page_count": ingestion_result["page_count"],
            "chunk_count": ingestion_result["chunk_count"],
            "stored_count": ingestion_result["stored_count"],
            "status": "indexed"
        }

    except Exception:
        logger.exception(
            "Document upload failed | filename=%s | document_id=%s",
            original_filename,
            document_id
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to upload and index document."
        )