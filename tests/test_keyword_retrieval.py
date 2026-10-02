from app.services.keyword_retrieval import KeywordRetriever


def test_keyword_retriever_returns_exact_keyword_match_first():
    chunks = [
        {
            "document_id": "doc-1",
            "chunk_index": 0,
            "source": "course.pdf",
            "page": 2,
            "text": "INFO5990 prepares students for an interactive oral viva"
        },
        {
            "document_id": "doc-2",
            "chunk_index": 0,
            "source": "docker.pdf",
            "page": 1,
            "text": "Docker packages applications into containers"
        },
        {
            "document_id": "doc-3",
            "chunk_index": 0,
            "source": "fastapi.pdf",
            "page": 1,
            "text": "FastAPI is used to build web APIs"
        },
        {
            "document_id": "doc-4",
            "chunk_index": 0,
            "source": "vector.pdf",
            "page": 1,
            "text": "Vector databases store embeddings"
        }
    ]

    retriever = KeywordRetriever(chunks)

    results = retriever.search(
        query="INFO5990",
        limit=3
    )

    assert len(results) == 1
    assert results[0]["chunk"]["document_id"] == "doc-1"
    assert results[0]["score"] > 0