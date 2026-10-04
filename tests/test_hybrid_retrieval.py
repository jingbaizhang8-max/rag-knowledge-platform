import app.services.hybrid_retrieval as hybrid


def test_rrf_rewards_chunk_found_by_both_retrievers(monkeypatch):

    chunk_a = {
        "document_id": "doc-1",
        "chunk_index": 0,
        "source": "a.pdf",
        "page": 1,
        "text": "INFO5990 oral viva"
    }

    chunk_b = {
        "document_id": "doc-1",
        "chunk_index": 1,
        "source": "a.pdf",
        "page": 2,
        "text": "Vector search content"
    }

    chunk_c = {
        "document_id": "doc-1",
        "chunk_index": 2,
        "source": "a.pdf",
        "page": 3,
        "text": "Keyword search content"
    }

    # 假装 Vector Search 返回 A、B
    def fake_vector_retrieve(
        query,
        limit,
        document_id=None
    ):
        return [
            {
                **chunk_a,
                "score": 0.9
            },
            {
                **chunk_b,
                "score": 0.8
            }
        ]

    # 假装 Qdrant 里有这三个 chunks
    def fake_get_all_chunks():
        return [chunk_a, chunk_b, chunk_c]

    class FakeKeywordRetriever:

        def __init__(self, chunks):
            self.chunks = chunks

        def search(self, query, limit):
            # BM25 返回 A、C
            return [
                {
                    "score": 5.0,
                    "chunk": chunk_a
                },
                {
                    "score": 4.0,
                    "chunk": chunk_c
                }
            ]

    monkeypatch.setattr(
        hybrid,
        "retrieve_chunks",
        fake_vector_retrieve
    )

    monkeypatch.setattr(
        hybrid,
        "get_all_chunks",
        fake_get_all_chunks
    )

    monkeypatch.setattr(
        hybrid,
        "KeywordRetriever",
        FakeKeywordRetriever
    )

    results = hybrid.hybrid_retrieve(
        query="INFO5990",
        limit=3,
        candidate_limit=10
    )

    assert results[0]["chunk"]["document_id"] == "doc-1"
    assert results[0]["chunk"]["chunk_index"] == 0

    assert results[0]["vector_rank"] == 1
    assert results[0]["bm25_rank"] == 1

    assert results[0]["rrf_score"] > results[1]["rrf_score"]