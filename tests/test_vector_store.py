
from app.services.embedding_service import  embed_texts

from app.services.vector_store import store_chunks
from qdrant_client import QdrantClient
import app.services.vector_store as vector_store


def test_store_chunks_returns_count():
    chunks=[
        {
            "document_id": "test-doc",
            "chunk_index": 0,
            "source": "test.txt",
            "page": None,
            "text": "RAG combines retrieval with generation."
        }
    ]

    embeddings = embed_texts(
        [chunk["text"] for chunk in chunks]
    )

    count = store_chunks(
        chunks = chunks,
        embeddings=embeddings
    )

    assert count==1

def test_search_chunks_filters_by_document_id(
        tmp_path,
        monkeypatch
):
    test_client = QdrantClient(
        path=str(tmp_path/"qdrant")
    )

    monkeypatch.setattr(
        vector_store,
        "qdrant_client",
        test_client
    )

    chunks = [
        {
            "document_id": "doc-a",
            "chunk_index": 0,
            "source": "a.pdf",
            "page": 1,
            "text": "This text belongs to document A."
        },
        {
            "document_id": "doc-b",
            "chunk_index": 0,
            "source": "b.pdf",
            "page": 1,
            "text": "This text belongs to document B."
        }
    ]

    test_vector = [0.0] * 384
    test_vector[0] = 1.0

    embeddings=[
        test_vector,
        test_vector
    ]

    vector_store.store_chunks(
        chunks=chunks,
        embeddings=embeddings
    )

    results=vector_store.search_chunks(
        query_vector=test_vector,
        limit=10,
        document_id="doc-a"
    )

    assert len(results) == 1
    assert results[0]["document_id"] == "doc-a"
    assert results[0]["source"] =="a.pdf"

    test_client.close()