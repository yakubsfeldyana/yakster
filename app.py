import streamlit as st
from openai import OpenAI
import os

# Set up OpenAI client with your API key
client = OpenAI(api_key="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")

import streamlit as st
from openai import OpenAI
import os

# 🔑 Set up OpenAI client
client = OpenAI(api_key="your-openai-key-here")  # <-- Replace with your real key

# 🎨 Page config
st.set_page_config(page_title="Yakster AI Chat", page_icon="🧠")

# ⬅️ Sidebar
with st.sidebar:

    st.title("🧠 Yakster")
    st.markdown("Your personal GPT-powered assistant. Upload files, get summaries, fix code, or just chat.")
    st.markdown("---")
    st.caption("Built by Yana — Future AI Dev 💻")

# 🎭 Choose personality
personality = st.selectbox("Choose a personality:", [
    "Helpful Assistant",
    "Sarcastic Friend",
    "Python Tutor",
    "Startup Coach",
    "Therapist",
    "Custom..."
])

if personality == "Custom...":
    custom_prompt = st.text_area("Write your custom personality:", height=100)
    if not custom_prompt:
        custom_prompt = "You are a helpful assistant."
else:
    personality_prompts = {
        "Helpful Assistant": "You are a helpful and friendly assistant.",
        "Sarcastic Friend": "You are a sarcastic and witty AI friend. Be funny but still helpful.",
        "Python Tutor": "You are a patient Python tutor. Explain everything in simple terms with code examples.",
        "Startup Coach": "You are a sharp startup coach. Give concise and strategic business advice.",
        "Therapist": "You are a compassionate therapist. Ask thoughtful questions and respond with empathy."
    }
    custom_prompt = personality_prompts[personality]

# 🧠 Initialize session memory
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": custom_prompt}]

# 📁 File Upload + Smart Tasks
uploaded_file = st.file_uploader("📁 Upload a .txt file", type=["txt"])

if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    st.text_area("📄 File Preview", file_content, height=200)

    task = st.radio("💡 What do you want to do with the file?", [
        "Chat with it",
        "Summarize it",
        "Fix the code",
        "Generate quiz"
    ])

    if task == "Summarize it":
        st.markdown("🧠 GPT is summarizing...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional summarizer."},
                {"role": "user", "content": f"Summarize this:\n\n{file_content}"}
            ]
        )
        st.success(response.choices[0].message.content)

    elif task == "Fix the code":
        st.markdown("🛠 Fixing the code...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're an expert Python code fixer."},
                {"role": "user", "content": f"Fix this code:\n\n{file_content}"}
            ]
        )
        st.code(response.choices[0].message.content, language="python")

    elif task == "Generate quiz":
        st.markdown("✍️ Generating quiz questions...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a teacher creating a quiz."},
                {"role": "user", "content": f"Create 5 quiz questions (with answers) based on this text:\n\n{file_content}"}
            ]
        )
        st.success(response.choices[0].message.content)

# 💬 Regular Chat Input
user_input = st.chat_input("💬 Ask anything...")

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
