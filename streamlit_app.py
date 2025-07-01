import os
import streamlit as st
import requests
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Calendent - Calendar Assistant",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }

    .user-message {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.8rem 0;
        margin-left: 15%;
        text-align: right;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
    }

    .bot-message {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        color: #333;
        padding: 0.8rem 1.2rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.8rem 0;
        margin-right: 15%;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .welcome-container {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
    }

    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #007bff;
        padding: 0.8rem 1rem;
    }

    .stButton > button {
        border-radius: 25px;
        width: 100%;
        background: linear-gradient(135deg, #007bff, #0056b3);
        border: none;
        color: white;
        font-weight: bold;
        padding: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = os.getenv("BACKEND_URL", "https://calendent.onrender.com")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hello! I'm TailorTalk, your calendar assistant. I can help you book appointments, check availability, and manage your schedule. Just tell me what you'd like to schedule!"
    })

if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"

if "processing" not in st.session_state:
    st.session_state.processing = False


def send_message(message):
    if not st.session_state.processing:
        st.session_state.messages.append({"role": "user", "content": message})
        st.session_state.processing = True
        st.rerun()


st.markdown("""
<div class="welcome-container">
    <h1>Calendent</h1>
    <p><strong>Your AI Calendar Assistant (IST Timezone)</strong></p>
    <p>Smart scheduling through natural conversation</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🚀 Features")
    st.markdown("- 📅 **IST Timezone Support**")
    st.markdown("- 🤖 **Smart Booking**")
    st.markdown("- ⚡ **Quick Actions**")
    st.markdown("- 💡 **Context Aware**")

    st.markdown("---")
    st.markdown("### 💬 Examples")
    st.markdown("- 'Book meeting tomorrow 2 PM'")
    st.markdown("- 'Schedule call next Tuesday 10 AM'")
    st.markdown("- 'What's free this Friday?'")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.processing = False
        st.rerun()

col1, col2, col3 = st.columns([0.5, 4, 0.5])

with col2:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            content = message["content"]

            if "🎉 SUCCESS!" in content:
                st.success("🎉 Booking Successful!")

            st.markdown(f"""
            <div class="bot-message">
                <strong>🤖 TailorTalk:</strong> {content}
            </div>
            """, unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_button = st.columns([5, 1])

        with col_input:
            user_input = st.text_input(
                "Type your message...",
                placeholder="e.g., 'Book team meeting tomorrow 2 PM'",
                label_visibility="collapsed"
            )

        with col_button:
            send_button = st.form_submit_button("Send 📤")

    if send_button and user_input.strip():
        send_message(user_input)

    if st.session_state.processing:
        last_user_message = None
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        if last_user_message:
            with st.spinner("🧠 Processing..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/chat",
                        json={
                            "message": last_user_message,
                            "user_id": st.session_state.user_id
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        data = response.json()
                        bot_response = data["response"]

                        if data.get("booking_success"):
                            st.balloons()

                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    else:
                        error_msg = f"❌ Server Error: {response.text}"
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                except Exception as e:
                    error_msg = f"❌ Connection error: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

                st.session_state.processing = False
                st.rerun()

st.markdown("### ⚡ Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📅 Today's Schedule", key="today"):
        send_message("What's my schedule for today?")

with col2:
    if st.button("🔍 Tomorrow Free?", key="tomorrow"):
        send_message("What's my availability tomorrow?")

with col3:
    if st.button("📞 Quick Meeting", key="meeting"):
        send_message("Book a 30-minute meeting tomorrow afternoon")

with col4:
    if st.button("📊 This Week", key="week"):
        send_message("Show me this week's availability")

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666;">
    <p>🕐 <strong>Working in IST Timezone</strong> | User ID: {st.session_state.user_id}</p>
    <p>Built using Streamlit & FastAPI</p>
</div>
""", unsafe_allow_html=True)
