
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4
from app.services.ingestion_service import ingest_document

router = APIRouter()
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


@router.post("/upload")
async def upload_document(
        file: UploadFile=File(...)
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

    content = await file.read()
    with open(file_path, "wb") as saved_file:
        saved_file.write(content)

    ingestion_result = ingest_document(
        file_path = file_path,
        document_id=document_id,
        source=original_filename
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