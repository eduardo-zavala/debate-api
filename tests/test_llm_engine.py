import pytest
from app.llm_engine import LLMEngine

def test_init_without_api_key_uses_mock(monkeypatch):
    monkeypatch.setattr("app.llm_engine.properties", type("P", (), {"GROQ_API_KEY": None})())
    eng = LLMEngine()
    assert eng.use_llm is False
    assert eng.api_key is None

def test_extract_debate_topic_mock(monkeypatch):
    monkeypatch.setattr("app.llm_engine.properties", type("P", (), {"GROQ_API_KEY": None})())
    eng = LLMEngine()
    out = eng.extract_debate_topic("Any message")
    assert out == {
        "topic": "General debate",
        "position": "I will argue against your position",
    }

def test_generate_debate_response_mock_deterministic(monkeypatch):
    monkeypatch.setattr("random.choice", lambda seq: seq[0])
    monkeypatch.setattr("app.llm_engine.properties", type("P", (), {"GROQ_API_KEY": None})())
    eng = LLMEngine()

    msg = eng.generate_debate_response(
        topic="Energy",
        position="pro nuclear",
        history=[],               
        user_message="Hi there", 
    )
    assert msg == "Regarding Energy, I firmly believe that pro nuclear."