from pathlib import Path

from app.services.chunker import chunk_pages
from app.services.document_parser import parse_document
from app.services.embedding_service import embed_texts
from app.services.vector_store import store_chunks

def ingest_document(
        file_path: Path,
        document_id: str,
        source: str
) -> dict:
    pages = parse_document(file_path)

    chunks = chunk_pages(
        pages=pages,
        document_id=document_id,
        source=source
    )

    texts = [
        chunk["text"] for chunk in chunks
    ]

    embeddings = embed_texts(texts)

    stored_count = store_chunks(
        chunks=chunks,
        embeddings=embeddings
    )

    return {
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "stored_count": stored_count
    }
