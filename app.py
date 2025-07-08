import streamlit as st
import os
from openai import OpenAI
from anthropic import Anthropic


# ✅ Set up Streamlit
st.set_page_config(page_title="Multi-AI Chatbot", page_icon="🤖")
st.title("🤖 Your Multi-AI Assistant")

# ✅ Choose AI model
ai_choice = st.selectbox("Choose your AI model:", ["ChatGPT (OpenAI)", "Claude (Anthropic)"])

# ✅ Choose personality
personality = st.selectbox("Pick a personality:", [
    "Helpful Assistant",
    "Sarcastic Friend",
    "History Tutor",
    "Startup Coach",
    "Therapist",
    "Custom..."
])

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

# ✅ Choose task
task = st.radio("What do you want to do?", ["Ask a question", "Summarize a file"])

# ✅ Handle input
if task == "Ask a question":
    user_input = st.chat_input("Ask your question...")
else:
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "md", "pdf"])
    user_input = ""
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            from PyPDF2 import PdfReader
            reader = PdfReader(uploaded_file)
            file_content = "\n\n".join(page.extract_text() for page in reader.pages)
        else:
            file_content = uploaded_file.read().decode("utf-8")
        user_input = f"Please summarize this:\n\n{file_content}"

# ✅ Always show personality in sidebar
st.sidebar.markdown(f"🧠 Active personality: **{personality}**")

# ✅ Always reset system prompt if changed
if "messages" not in st.session_state or st.session_state.messages[0]["content"] != custom_prompt:
    st.session_state.messages = [{"role": "system", "content": custom_prompt}]

# ✅ When user sends a message or file
if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        if ai_choice == "ChatGPT (OpenAI)":
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        else:
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": user_input}]
            )
            reply = response.content[0].text

        st.chat_message("assistant").write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"❌ Error: {e}")
