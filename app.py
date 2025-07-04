import streamlit as st
from openai import OpenAI
import os

# Set up OpenAI client with your API key
client = OpenAI(api_key="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")

# Streamlit page config
st.set_page_config(page_title="GPT Chatbot", page_icon="🤖")

st.title("🤖 GPT Chatbot (Web)")
# Let user pick a personality
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




st.caption("Built by you — future AI dev 💻")

# Session state to hold chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": custom_prompt}
    ]


# Chat input box
user_input = st.chat_input("Say something...")

uploaded_file = st.file_uploader("Upload a .txt file", type="txt")

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    st.text_area("📄 File contents", file_content, height=200)

    # Add the content to the start of the chat as context
    st.session_state.messages.insert(1, {
        "role": "user",
        "content": f"Here's the file content:\n\n{file_content}"
    })

    st.success("✅ File content added to the chat. Now ask questions about it!")


if user_input:
    # Show user message
    st.chat_message("user").write(user_input)

    # Add to chat memory
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Send to GPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

        # Show assistant reply
        st.chat_message("assistant").write(reply)

        # Add assistant reply to memory
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"❌ Error: {e}")
