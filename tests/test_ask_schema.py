from app.schemas.ask import AskRequest


def test_ask_request_accepts_document_id():
    request = AskRequest(
        query="What is RAG?",
        limit=3,
        document_id="doc-123"
    )

    assert request.query == "What is RAG?"
    assert request.limit == 3
    assert request.document_id == "doc-123"


def test_document_id_is_optional():
    request = AskRequest(
        query="What is RAG?"
    )

    assert request.document_id is None