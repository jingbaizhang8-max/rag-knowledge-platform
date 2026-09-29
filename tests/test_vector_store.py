from app.services.embedding_service import  embed_texts

from app.services.vector_store import store_chunks

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