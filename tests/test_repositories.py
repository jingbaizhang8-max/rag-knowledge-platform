import pytest

from app.services.document_repository import create_document_record
from app.services.query_history_repository import create_query_history


class FakeSession:
    def __init__(self):
        self.rollback_called = False

    def add(self, obj):
        pass

    def commit(self):
        raise RuntimeError("Database commit failed")

    def refresh(self, obj):
        pass

    def rollback(self):
        self.rollback_called = True


def test_document_repository_rolls_back_on_commit_failure():
    db = FakeSession()

    with pytest.raises(RuntimeError):
        create_document_record(
            db=db,
            document_id="doc-1",
            filename="test.pdf",
            page_count=10,
            chunk_count=20,
            status="indexed"
        )

    assert db.rollback_called is True


def test_query_history_repository_rolls_back_on_commit_failure():
    db = FakeSession()

    with pytest.raises(RuntimeError):
        create_query_history(
            db=db,
            query="test question",
            answer="test answer",
            document_id=None,
            sources=[]
        )

    assert db.rollback_called is True