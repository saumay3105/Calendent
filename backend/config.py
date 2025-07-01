import os
from dotenv import load_dotenv
import pytz

load_dotenv()


class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    CALENDAR_ID = os.getenv("CALENDAR_ID")
    IST = pytz.timezone("Asia/Kolkata")
    HOST = "0.0.0.0"
    PORT = 8001
    MAX_CONVERSATION_HISTORY = 20
    RECENT_MESSAGES_LIMIT = 6


settings = Settings()
