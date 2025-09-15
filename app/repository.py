from typing import Optional, List, Dict
from .models import Message
from .properties import properties

class ConversationRepository:

    def __init__(self):
            self.memory_storage = {}
    
    def save_conversation(self, conversation_id: str, messages: List[Message]):
        messages_dict = [
            {"role": msg.role, "message": msg.message} 
            for msg in messages
        ]
        
        self.memory_storage[conversation_id] = messages_dict
    
    def get_conversation(self, conversation_id: str) -> Optional[List[Message]]:

        messages_dict = self.memory_storage.get(conversation_id)
        if messages_dict:
            return [Message(**msg) for msg in messages_dict]
        
        return None
    
    def exists(self, conversation_id: str) -> bool:
        
        return conversation_id in self.memory_storage
    
    def delete_conversation(self, conversation_id: str):
        
        self.memory_storage.pop(conversation_id, None)

conversation_repository = ConversationRepository()