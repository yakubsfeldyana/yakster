import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API keys from .env
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

# Streamlit page setup
st.set_page_config(page_title="GPT Chatbot", page_icon="🤖")
st.title("🤖 OpenAI Chatbot")

# Choose personality
personality = st.selectbox("Pick a personality:", [
    "Helpful Assistant",
    "Sarcastic Friend",
    "History Tutor",
    "Startup Coach",
    "Therapist",
    "Custom..."
])

# Set prompt based on personality
if personality == "Custom...":
    custom_prompt = st.text_area("Describe your custom personality:", height=100)
    if not custom_prompt:
        custom_prompt = "You are a helpful assistant."
else:
    prompts = {
        "Helpful Assistant": "You are a helpful and friendly assistant.",
        "Sarcastic Friend": "You are a sarcastic and witty AI friend. Be funny but helpful.",
        "History Tutor": "You are a patient History tutor. Explain in simple terms.",
        "Startup Coach": "You are a sharp startup coach. Give strategic and concise advice.",
        "Therapist": "You are a compassionate therapist. Ask questions, respond with empathy."
    }
    custom_prompt = prompts[personality]

# Task choice
task = st.radio("What do you want to do?", ["Ask a question", "Summarize a file"])

# Sidebar info
st.sidebar.markdown(f"🧠 Active personality: **{personality}**")

# Ensure messages start with the selected personality
if "messages" not in st.session_state or st.session_state.messages[0]["content"] != custom_prompt:
    st.session_state.messages = [{"role": "system", "content": custom_prompt}]

# Get user input or summarize uploaded file
user_input = ""
if task == "Ask a question":
    user_input = st.chat_input("Ask your question...")
else:
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "md", "pdf"])
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            from PyPDF2 import PdfReader
            reader = PdfReader(uploaded_file)
            file_content = "\n\n".join(page.extract_text() for page in reader.pages)
        else:
            file_content = uploaded_file.read().decode("utf-8")
        user_input = f"Please summarize this:\n\n{file_content}"
    else:
        st.stop()

# Process input and show response
if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

        st.chat_message("assistant").write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"❌ Error: {e}")
