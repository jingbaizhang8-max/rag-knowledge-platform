import app.services.reranker_service as reranker


class FakeModel:
    def predict(self, pairs):
        return [0.2, 0.9, 0.5]


def test_rerank_chunks_sorts_by_rerank_score(monkeypatch):

    candidates = [
        {
            "chunk": {
                "document_id": "doc-1",
                "chunk_index": 0,
                "source": "a.pdf",
                "page": 1,
                "text": "chunk A"
            },
            "vector_score": 0.9,
            "bm25_score": None,
            "rrf_score": 0.03,
            "vector_rank": 1,
            "bm25_rank": None
        },
        {
            "chunk": {
                "document_id": "doc-1",
                "chunk_index": 1,
                "source": "a.pdf",
                "page": 2,
                "text": "chunk B"
            },
            "vector_score": 0.8,
            "bm25_score": 2.0,
            "rrf_score": 0.04,
            "vector_rank": 2,
            "bm25_rank": 1
        },
        {
            "chunk": {
                "document_id": "doc-1",
                "chunk_index": 2,
                "source": "a.pdf",
                "page": 3,
                "text": "chunk C"
            },
            "vector_score": 0.7,
            "bm25_score": None,
            "rrf_score": 0.02,
            "vector_rank": 3,
            "bm25_rank": None
        }
    ]

    monkeypatch.setattr(
        reranker,
        "get_reranker",
        lambda: FakeModel()
    )

    results = reranker.rerank_chunks(
        query="test query",
        candidates=candidates,
        limit=2
    )

    assert len(results) == 2

    assert results[0]["chunk"]["text"] == "chunk B"
    assert results[0]["rerank_score"] == 0.9

    assert results[1]["chunk"]["text"] == "chunk C"
    assert results[1]["rerank_score"] == 0.5