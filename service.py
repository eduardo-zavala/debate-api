import uuid
import random
from typing import Optional, Dict, List
from models import DebateRequest, DebateResponse, Message
from repository import conversation_repository  # Agregar import

class DebateService:

    def __init__(self):
        self.repository = conversation_repository
    
    def debate(self, request: DebateRequest) -> DebateResponse:
        
        if request.conversation_id is None:
            conversation_id = self._create_new_conversation(request.message)
        else:
            conversation_id = self._continue_conversation(
                request.conversation_id, 
                request.message
            )
        
        messages = self._get_last_messages(conversation_id, limit=5)
        
        return DebateResponse(
            conversation_id=conversation_id,
            message=messages
        )
    
    def _create_new_conversation(self, user_message: str) -> str:
        conversation_id = str(uuid.uuid4())
        
        messages = [
            Message(role="user", message=user_message)
        ]
        
        bot_response = self._generate_bot_response(user_message, [])
        messages.append(Message(role="bot", message=bot_response))
        
        self.repository.save_conversation(conversation_id, messages)
        
        return conversation_id
    
    def _continue_conversation(self, conversation_id: str, user_message: str) -> str:
        messages = self.repository.get_conversation(conversation_id)
        
        if messages is None:
            print(f"Conversation {conversation_id} not found, creating new one")
            return self._create_new_conversation(user_message)
        
        messages.append(Message(role="user", message=user_message))
        
        bot_response = self._generate_bot_response(user_message, messages)
        messages.append(Message(role="bot", message=bot_response))
        
        self.repository.save_conversation(conversation_id, messages)
        
        return conversation_id
    
    def _generate_bot_response(self, user_message: str, history: List[Message]) -> str:

        responses = [
            "I strongly disagree with that perspective.",
            "That's an interesting point, but have you considered the opposite?",
            "The evidence clearly supports a different conclusion.",
            "I maintain my position despite your argument.",
            "Your logic has flaws that I must point out."
        ]
        
        return random.choice(responses)
    
    def _get_last_messages(self, conversation_id: str, limit: int = 5) -> List[Message]:
        messages = self.repository.get_conversation(conversation_id)
        
        if messages is None:
            return []
        
        return messages[-limit:] if len(messages) > limit else messages

debate_service = DebateService()