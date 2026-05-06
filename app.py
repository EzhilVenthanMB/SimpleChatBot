import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import json

# Load env
load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# File to store chat history
HISTORY_FILE = "chat_history.json"

# Function to load history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return [{"role": "system", "content": "You are a helpful assistant."}]

# Function to save history
def save_history(messages):
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f)

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot with History")

# Load messages into session
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# Display chat
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get AI response
    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model="llama-3.1-8b-instant"
    )

    reply = response.choices[0].message.content

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

    # Save history
    save_history(st.session_state.messages)

# Clear history button
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    save_history(st.session_state.messages)
    st.rerun()