from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "default_user"

class ChatResponse(BaseModel):
    response: str
    booking_success: Optional[bool] = None
