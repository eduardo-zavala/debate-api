from pydantic import BaseModel
from typing import Optional, List

class DebateRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class Message(BaseModel):
    role: str 
    message: str

class DebateResponse(BaseModel):
    conversation_id: str
    message: List[Message]