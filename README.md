# Calendent

Calendent is a conversational AI calendar assistant that helps you manage your Google Calendar through natural language conversation. It can book appointments, check your availability, and suggest optimal meeting times—just tell it what you'd like to schedule!

## 🚀 Features

- 📅 **IST Timezone Support**  
  All scheduling is handled in the Indian Standard Time (IST) zone.

- 🤖 **Smart Booking**  
  Book meetings, appointments, or events quickly with natural language requests.

- ⚡ **Quick Actions**  
  Instantly check today's schedule, tomorrow's availability, or your free slots this week with a single click.

- 💡 **Context-Aware**  
  Understands phrases like "tomorrow", "this Friday", "next week", and more to provide accurate scheduling.

- 📝 **Google Calendar Integration**  
  Securely interacts with your Google Calendar using service account credentials.

## 💬 Example Commands

- `"Book meeting tomorrow 2 PM"`
- `"Schedule call next Tuesday 10 AM"`
- `"What's free this Friday?"`
- `"Show me this week's availability"`

## 🏗️ How It Works

- **Frontend**: Built using [Streamlit](https://streamlit.io/), providing an interactive chat interface for users to converse with the AI assistant.
- **Backend**: Powered by [FastAPI](https://fastapi.tiangolo.com/), exposes a REST API that processes user messages and interacts with Google Calendar via service account credentials.
- **AI Agent**: Uses a prompt-based system to interpret user intent, extract event details, check availability, and book events as needed.
- **IST Timezone**: All operations are performed in the IST timezone for seamless scheduling in India.

## 🛠️ Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/saumay3105/Calendent.git
    cd Calendent
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Environment setup**
    - Create a `.env` file in the root directory.
    - Add your Google Service Account credentials and calendar ID as environment variables:
        ```
        GOOGLE_SERVICE_ACCOUNT_FILE=path/to/credentials.json
        CALENDAR_ID=your_calendar_id@group.calendar.google.com
        GOOGLE_API_KEY=your_api_key
        ```

4. **Run the backend**
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```

5. **Run the frontend**
    ```bash
    streamlit run streamlit_app.py
    ```

6. **Open in your browser:**
    ```
    http://localhost:8501
    ```

## 🧩 Project Structure

```
Calendent/
├── backend/                # FastAPI backend service
│   ├── api/                # API routes
│   ├── agents/             # Conversational agent logic
│   ├── services/           # Calendar and conversation services
│   ├── tools/              # Calendar interaction tools
│   └── main.py             # Entry point for backend
├── streamlit_app.py        # Streamlit frontend
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 📦 Dependencies

- FastAPI
- Streamlit
- Google API Python Client
- LangChain
- Requests
- Pydantic
- Python-dotenv
- Uvicorn
- pytz
- httpx

(See `requirements.txt` for complete list.)

## 🛡️ Security

- Uses Google Service Account for secure calendar access.
- CORS enabled for frontend-backend communication.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Calendar API](https://developers.google.com/calendar)
- [LangChain](https://python.langchain.com/)

