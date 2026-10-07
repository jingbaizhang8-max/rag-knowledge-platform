import pytest
from fastapi import HTTPException

import app.api.ask as ask_api
from app.schemas.ask import AskRequest


def test_ask_returns_500_when_internal_error_occurs(monkeypatch):

    def fake_ask_question(
        query,
        limit,
        document_id=None
    ):
        raise RuntimeError("Internal RAG failure")

    monkeypatch.setattr(
        ask_api,
        "ask_question",
        fake_ask_question
    )

    request = AskRequest(
        query="test question",
        limit=3
    )

    with pytest.raises(HTTPException) as error:
        ask_api.ask(
            request=request,
            db=None
        )

    assert error.value.status_code == 500
    assert error.value.detail == (
        "Failed to process question."
    )