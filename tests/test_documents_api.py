from app.api import documents as documents_api


class FakeDocument:
    document_id = "test-document-id"
    filename = "test.pdf"
    page_count = 5
    chunk_count = 10
    status = "indexed"


def test_list_documents_returns_document_metadata(monkeypatch):
    monkeypatch.setattr(
        documents_api,
        "list_document_records",
        lambda db: [FakeDocument()],
    )

    result = documents_api.list_documents(db=None)

    assert result == [
        {
            "document_id": "test-document-id",
            "filename": "test.pdf",
            "page_count": 5,
            "chunk_count": 10,
            "status": "indexed",
        }
    ]