from types import SimpleNamespace

import app.services.evidence_verifier as verifier


def test_has_sufficient_evidence_returns_true_for_yes(monkeypatch):

    fake_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="YES"
                )
            )
        ]
    )

    def fake_create(*args, **kwargs):
        return fake_response

    monkeypatch.setattr(
        verifier.client.chat.completions,
        "create",
        fake_create
    )

    result = verifier.has_sufficient_evidence(
        query="What is missing from the status update?",
        context="It lacks cause, impact, timing and next action."
    )

    assert result is True


def test_has_sufficient_evidence_returns_false_for_no(monkeypatch):

    fake_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="NO"
                )
            )
        ]
    )

    def fake_create(*args, **kwargs):
        return fake_response

    monkeypatch.setattr(
        verifier.client.chat.completions,
        "create",
        fake_create
    )

    result = verifier.has_sufficient_evidence(
        query="Which model has the highest success rate?",
        context="Kotter guides mobilisation. ADKAR tracks adoption."
    )

    assert result is False


def test_has_sufficient_evidence_skips_llm_for_empty_context(
    monkeypatch
):

    def fake_create(*args, **kwargs):
        raise AssertionError(
            "LLM should not be called for empty context"
        )

    monkeypatch.setattr(
        verifier.client.chat.completions,
        "create",
        fake_create
    )

    result = verifier.has_sufficient_evidence(
        query="Anything?",
        context="   "
    )

    assert result is False