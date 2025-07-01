from fastapi import APIRouter, HTTPException
from datetime import datetime
from backend.models.chat import ChatMessage, ChatResponse
from backend.services.conversation_service import ConversationService
from backend.services.date_parser import DateParser
from backend.agents.chat_agent import ChatAgent
from backend.config import settings

router = APIRouter()
conversation_service = ConversationService()
date_parser = DateParser()
chat_agent = ChatAgent()

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        current_date = datetime.now(settings.IST).strftime("%Y-%m-%d")
        user_id = message.user_id

        context = conversation_service.get_context(user_id)
        conversation_service.update_history(user_id, "user", message.message)

        processed_message = message.message
        if any(word in message.message.lower() for word in ["tomorrow", "friday", "this week", "next week"]):
            suggested_date = date_parser.parse_natural_date(message.message, current_date)
            processed_message = f"{message.message} (Date context: {suggested_date})"

        bot_response = chat_agent.process_message(processed_message, current_date, context)
        conversation_service.update_history(user_id, "assistant", bot_response)

        booking_success = "🎉 SUCCESS!" in bot_response

        return ChatResponse(
            response=bot_response,
            booking_success=booking_success
        )

    except Exception as e:
        error_response = f"❌ I encountered an error: {str(e)}. Please try again."
        conversation_service.update_history(message.user_id, "assistant", error_response)
        raise HTTPException(status_code=500, detail=error_response)

@router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(settings.IST).isoformat()}
