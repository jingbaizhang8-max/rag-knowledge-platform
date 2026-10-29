
from importlib import import_module

from fastapi.testclient import TestClient
from app.main import app


def test_search_passes_document_id(monkeypatch):
    search_api = import_module("app.api.search")
    captured = {}

    def fake_retrieve_chunks(
        query,
        limit,
        document_id=None,
    ):
        captured["query"] = query
        captured["limit"] = limit
        captured["document_id"] = document_id
        return []

    monkeypatch.setattr(
        search_api,
        "retrieve_chunks",
        fake_retrieve_chunks,
    )

    client = TestClient(app)

    response = client.post(
        "/search",
        json={
            "query": "退款政策",
            "limit": 5,
            "document_id": "test-document-001",
        },
    )

    assert response.status_code == 200
    assert captured["document_id"] == "test-document-001"
    assert captured["limit"] == 5
    assert response.json()["results"] == []
