import uuid
import pytest

from app.models import DebateRequest, Message
from app.service import DebateService


# --------- Fakes / Stubs ---------
class FakeRepo:
    """In-memory repo that mimics save/get for conversations."""
    def __init__(self):
        self.store = {}

    def save_conversation(self, conversation_id, messages):
        self.store[conversation_id] = list(messages)

    def get_conversation(self, conversation_id):
        return self.store.get(conversation_id)


class FakeLLM:
    """Fake LLM engine that provides deterministic outputs."""
    def __init__(self):
        self.extract_calls = []
        self.generate_calls = []

    def extract_debate_topic(self, user_message: str):
        self.extract_calls.append(user_message)
        return {"topic": "energy", "position": "pro-nuclear"}

    def generate_debate_response(self, *, topic, position, history, user_message):
        self.generate_calls.append(
            {"topic": topic, "position": position, "history_len": len(history), "user": user_message}
        )
        return f"[{topic}|{position}] reply to: {user_message}"


# --------- Fixtures ---------
@pytest.fixture
def service(monkeypatch):
    svc = DebateService()
    svc.repository = FakeRepo()
    svc.llm = FakeLLM()
    return svc


# --------- Tests ---------
def test_start_new_conversation_creates_and_saves(service, monkeypatch):
    fixed_uuid = uuid.UUID("00000000-0000-0000-0000-000000000001")
    monkeypatch.setattr("app.service.uuid.uuid4", lambda: fixed_uuid)

    req = DebateRequest(conversation_id=None, message="Let's debate nuclear energy")
    resp = service.process_debate(req)

    assert resp.conversation_id == str(fixed_uuid)
    assert len(resp.message) == 2
    assert resp.message[0].role == "user"
    assert resp.message[0].message == "Let's debate nuclear energy"
    assert resp.message[1].role == "bot"
    assert "[energy|pro-nuclear]" in resp.message[1].message

    stored = service.repository.get_conversation(resp.conversation_id)
    assert stored is not None and len(stored) == 2

    assert service.llm.extract_calls == ["Let's debate nuclear energy"]
    assert len(service.llm.generate_calls) == 1
    assert service.conversation_contexts[resp.conversation_id] == {"topic": "energy", "position": "pro-nuclear"}


def test_continue_conversation_appends_and_uses_context(service, monkeypatch):
    conv_id = "conv-123"
    service.conversation_contexts[conv_id] = {"topic": "energy", "position": "pro-nuclear"}
    service.repository.save_conversation(conv_id, [
        Message(role="user", message="Hi"),
        Message(role="bot",  message="Hello")
    ])

    req = DebateRequest(conversation_id=conv_id, message="I disagree")
    resp = service.process_debate(req)

    assert resp.conversation_id == conv_id
    assert resp.message[-1].role == "bot"
    assert "[energy|pro-nuclear]" in resp.message[-1].message

    stored = service.repository.get_conversation(conv_id)
    assert len(stored) == 4

    assert len(service.llm.generate_calls) >= 1
    last_call = service.llm.generate_calls[-1]
    assert last_call["topic"] == "energy"
    assert last_call["position"] == "pro-nuclear"


def test_continue_conversation_missing_id_creates_new(service, monkeypatch):
    missing_id = "does-not-exist"
    req = DebateRequest(conversation_id=missing_id, message="Start anyway")

    fixed_uuid = uuid.UUID("00000000-0000-0000-0000-00000000000A")
    monkeypatch.setattr("app.service.uuid.uuid4", lambda: fixed_uuid)

    resp = service.process_debate(req)
    assert resp.conversation_id == str(fixed_uuid)

    stored = service.repository.get_conversation(resp.conversation_id)
    assert stored is not None and len(stored) == 2

    assert service.llm.extract_calls == ["Start anyway"]


def test_get_last_messages_limit(service, monkeypatch):
    conv_id = "conv-limit"
    msgs = []
    for i in range(8):
        msgs.append(Message(role="user" if i % 2 == 0 else "bot", message=f"m{i}"))
    service.repository.save_conversation(conv_id, msgs)

    req = DebateRequest(conversation_id=conv_id, message="next")
    service.conversation_contexts[conv_id] = {"topic": "energy", "position": "pro-nuclear"}

    resp = service.process_debate(req)
    assert len(resp.message) == 5
    assert resp.message[-1].role == "bot"