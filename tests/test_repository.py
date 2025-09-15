import pytest
from app.models import Message
from app.repository import ConversationRepository


@pytest.fixture
def repo():
    return ConversationRepository()


def test_save_and_get_conversation(repo):
    conv_id = "conv-1"
    msgs = [
        Message(role="user", message="hello"),
        Message(role="bot", message="hi there"),
    ]

    repo.save_conversation(conv_id, msgs)
    result = repo.get_conversation(conv_id)

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(m, Message) for m in result)
    assert result[0].role == "user"
    assert result[1].message == "hi there"


def test_get_conversation_not_found(repo):
    result = repo.get_conversation("missing")
    assert result is None


def test_exists(repo):
    conv_id = "conv-2"
    assert repo.exists(conv_id) is False

    repo.save_conversation(conv_id, [Message(role="user", message="msg")])
    assert repo.exists(conv_id) is True


def test_delete_conversation(repo):
    conv_id = "conv-3"
    repo.save_conversation(conv_id, [Message(role="user", message="msg")])
    assert repo.exists(conv_id) is True

    repo.delete_conversation(conv_id)
    assert repo.exists(conv_id) is False
    assert repo.get_conversation(conv_id) is None


def test_delete_conversation_not_existing_does_not_error(repo):
    repo.delete_conversation("does-not-exist")
    assert repo.memory_storage == {}
