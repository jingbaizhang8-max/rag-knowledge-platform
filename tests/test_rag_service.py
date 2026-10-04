import app.services.rag_service as rag


def test_ask_question_uses_hybrid_and_reranker(monkeypatch):

    candidates = [
        {
            "chunk": {
                "document_id": "doc-1",
                "chunk_index": 0,
                "source": "course.pdf",
                "page": 1,
                "text": "INFO5990 is a Professional Practice in IT course."
            },
            "vector_score": 0.8,
            "bm25_score": 2.0,
            "rrf_score": 0.03,
            "vector_rank": 1,
            "bm25_rank": 1
        },
        {
            "chunk": {
                "document_id": "doc-1",
                "chunk_index": 1,
                "source": "course.pdf",
                "page": 2,
                "text": "This chunk is not relevant."
            },
            "vector_score": 0.4,
            "bm25_score": None,
            "rrf_score": 0.01,
            "vector_rank": 2,
            "bm25_rank": None
        }
    ]

    reranked_results = [
        {
            **candidates[0],
            "rerank_score": 4.0
        },
        {
            **candidates[1],
            "rerank_score": -3.0
        }
    ]

    def fake_hybrid_retrieve(
        query,
        limit,
        candidate_limit,
        document_id=None
    ):
        return candidates

    def fake_rerank_chunks(
        query,
        candidates,
        limit
    ):
        return reranked_results

    def fake_generate_answer(query, context):
        assert "INFO5990 is a Professional Practice" in context
        assert "not relevant" not in context

        return "INFO5990 is a Professional Practice in IT course."

    monkeypatch.setattr(
        rag,
        "hybrid_retrieve",
        fake_hybrid_retrieve
    )

    monkeypatch.setattr(
        rag,
        "rerank_chunks",
        fake_rerank_chunks
    )

    monkeypatch.setattr(
        rag,
        "generate_answer",
        fake_generate_answer
    )

    result = rag.ask_question(
        query="What is INFO5990?",
        limit=3,
        document_id="doc-1"
    )

    assert result["answer"] == (
        "INFO5990 is a Professional Practice in IT course."
    )

    assert len(result["retrieved_chunks"]) == 1

    assert result["sources"] == [
        {
            "source": "course.pdf",
            "page": 1
        }
    ]



def test_ask_question_skips_llm_when_no_relevant_chunks(monkeypatch):

    candidates = [
        {
            "chunk": {
                "document_id": "doc-1",
                "chunk_index": 0,
                "source": "course.pdf",
                "page": 1,
                "text": "Completely unrelated content."
            },
            "vector_score": 0.3,
            "bm25_score": None,
            "rrf_score": 0.01,
            "vector_rank": 1,
            "bm25_rank": None
        }
    ]

    reranked_results = [
        {
            **candidates[0],
            "rerank_score": -5.0
        }
    ]

    def fake_hybrid_retrieve(
        query,
        limit,
        candidate_limit,
        document_id=None
    ):
        return candidates

    def fake_rerank_chunks(
        query,
        candidates,
        limit
    ):
        return reranked_results

    def fake_generate_answer(query, context):
        raise AssertionError(
            "LLM should not be called when no relevant chunks exist"
        )

    monkeypatch.setattr(
        rag,
        "hybrid_retrieve",
        fake_hybrid_retrieve
    )

    monkeypatch.setattr(
        rag,
        "rerank_chunks",
        fake_rerank_chunks
    )

    monkeypatch.setattr(
        rag,
        "generate_answer",
        fake_generate_answer
    )

    result = rag.ask_question(
        query="What is the capital of France?",
        limit=3,
        document_id="doc-1"
    )

    assert result["answer"] == (
        "I don't know based on the provided context."
    )

    assert result["sources"] == []
    assert result["retrieved_chunks"] == []