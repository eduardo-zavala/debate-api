import uuid
from typing import List
from .models import DebateRequest, DebateResponse, Message
from .repository import conversation_repository 
from .llm_engine import llm_engine

class DebateService:

    def __init__(self):
        self.repository = conversation_repository
        self.llm = llm_engine
        self.conversation_contexts = {}

    def process_debate(self, request: DebateRequest) -> DebateResponse:

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
        
        debate_context = self.llm.extract_debate_topic(user_message)
        
        self.conversation_contexts[conversation_id] = debate_context
        
        messages = [
            Message(role="user", message=user_message)
        ]
        
        bot_response = self.llm.generate_debate_response(
            topic=debate_context["topic"],
            position=debate_context["position"],
            history=[],
            user_message=user_message
        )
        messages.append(Message(role="bot", message=bot_response))
        
        self.repository.save_conversation(conversation_id, messages)
        
        print(f"New debate - Topic: {debate_context['topic']}")
        print(f"Bot position: {debate_context['position']}")
        
        return conversation_id
    
    def _continue_conversation(self, conversation_id: str, user_message: str) -> str:

        messages = self.repository.get_conversation(conversation_id)
        
        if messages is None:
            print(f"Conversation {conversation_id} not found, creating new one")
            return self._create_new_conversation(user_message)
        
        context = self.conversation_contexts.get(conversation_id, {
            "topic": "the topic",
            "position": "my position"
        })
        
        messages.append(Message(role="user", message=user_message))
        
        bot_response = self.llm.generate_debate_response(
            topic=context["topic"],
            position=context["position"],
            history=messages,
            user_message=user_message
        )
        messages.append(Message(role="bot", message=bot_response))
        
        self.repository.save_conversation(conversation_id, messages)
        
        return conversation_id
    
    def _get_last_messages(self, conversation_id: str, limit: int = 10) -> List[Message]:
        messages = self.repository.get_conversation(conversation_id)
        
        if messages is None:
            return []
        
        return messages[-limit:] if len(messages) > limit else messages

debate_service = DebateService()