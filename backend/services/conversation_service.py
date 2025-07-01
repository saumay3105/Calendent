from typing import Dict, List
from datetime import datetime
from backend.config import settings

class ConversationService:
    def __init__(self):
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    def get_context(self, user_id: str) -> str:
        if user_id not in self.conversation_history:
            return ""

        recent_messages = self.conversation_history[user_id][-settings.RECENT_MESSAGES_LIMIT:]
        context = "Recent conversation:\n"
        for msg in recent_messages:
            context += f"{msg['role']}: {msg['content']}\n"
        return context
    
    def update_history(self, user_id: str, role: str, content: str):
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []

        self.conversation_history[user_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now(settings.IST).isoformat()
        })

        if len(self.conversation_history[user_id]) > settings.MAX_CONVERSATION_HISTORY:
            self.conversation_history[user_id] = self.conversation_history[user_id][-settings.MAX_CONVERSATION_HISTORY:]
