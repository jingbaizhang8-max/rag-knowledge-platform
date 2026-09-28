
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4
from app.services.document_parser import parse_document
from app.services.chunker import chunk_pages

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

    pages = parse_document(file_path)

    chunks = chunk_pages(
        pages=pages,
        document_id=document_id,
        source=original_filename
    )

    return {
        "document_id": document_id,
        "filename": original_filename,
        "content_type": file.content_type,
        "size": len(content),
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "status": "processed"
    }