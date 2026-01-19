import streamlit as st
import tempfile
import os
import io
import csv


from llm import generate_answer
from pdf_rag import load_pdf_text, split_text, create_faiss_index, get_pdf_answer
from voice_input import speech_to_text
from gtts import gTTS

from auth import signup_user, login_user
from chat_db import save_chat, load_chat
from database import create_tables

# ----------------- Initialize DB -----------------
create_tables()  # Ensure tables exist

# ----------------- Page Config -----------------
st.set_page_config(page_title="SmartKnowledge AI", layout="wide")
st.title("SmartKnowledge AI")
st.caption("Multimodal AI Assistant")

# ----------------- CUSTOM CSS (BACKGROUND + UI) -----------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Sidebar glass effect */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Headers */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 600;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}

/* User message */
[data-testid="stChatMessage"][aria-label="Chat message from user"] {
    background: linear-gradient(135deg, #1d976c, #93f9b9);
    color: black;
}

/* Assistant message */
[data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
    background: rgba(255, 255, 255, 0.12);
    color: white;
}

/* Input box */
input, textarea {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 12px !important;
}

/* Buttons */
button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border-radius: 12px !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)


# ----------------- Session State -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_index" not in st.session_state:
    st.session_state.pdf_index = None
    st.session_state.pdf_chunks = None

# ----------------- Authentication -----------------
if not st.session_state.logged_in:
    st.sidebar.subheader("Login / Signup")
    auth_tab = st.sidebar.tabs(["Login", "Signup"])
    
    with auth_tab[0]:
        login_user_input = st.text_input("Username", key="login_user")
        login_pass_input = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if login_user(login_user_input, login_pass_input):
                st.session_state.logged_in = True
                st.session_state.username = login_user_input
                st.session_state.chat_history = load_chat(st.session_state.username)
                st.success(f"Welcome back, {st.session_state.username}!")
            else:
                st.error("Invalid username or password.")

    with auth_tab[1]:
        signup_user_input = st.text_input("Username", key="signup_user")
        signup_pass_input = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Signup"):
            if signup_user(signup_user_input, signup_pass_input):
                st.success("Signup successful! You can now login.")
            else:
                st.error("Username already exists.")

    st.stop()

# ----------------- Helpers -----------------
def is_greeting(text):
    return text.lower().strip() in ["hi", "hello", "hey", "hii", "hola"]

def speak_text(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        st.audio(open(f.name, "rb").read(), format="audio/mp3")
    os.remove(f.name)

# ----------------- Sidebar (ChatGPT Style) -----------------
with st.sidebar:
    st.subheader("Chat History")
    if st.session_state.chat_history:
        for i, (user_msg, bot_msg) in enumerate(reversed(st.session_state.chat_history), 1):
            st.markdown(f"**You:** {user_msg}")
            st.markdown(f"**Bot:** {bot_msg}")
            st.divider()
     else:
        st.info("No chat history yet.")

    # Download chat history button
    if st.session_state.chat_history:
        history_text = ""
        for user_msg, bot_msg in st.session_state.chat_history:
            history_text += f"You: {user_msg}\nBot: {bot_msg}\n\n"
        st.download_button(
            label="Download Chat History",
            data=history_text,
            file_name=f"{st.session_state.username}_chat_history.txt",
            mime="text/plain"
        )


    st.subheader("PDF & Settings")
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    use_pdf = st.checkbox("Use PDF for answers", value=True)
    voice_output = st.checkbox("Play answer in voice")

# ----------------- PDF Processing -----------------
if pdf_file:
    with st.spinner("Processing PDF..."):
        pdf_text = load_pdf_text(pdf_file)
        chunks = split_text(pdf_text)
        index, chunks = create_faiss_index(chunks)

        st.session_state.pdf_index = index
        st.session_state.pdf_chunks = chunks

    st.success("PDF processed successfully!")
    st.info("PDF uploaded. Answers will be taken ONLY from the PDF.")

if not use_pdf:
    st.session_state.pdf_index = None
    st.session_state.pdf_chunks = None

# ----------------- Main Chat Area -----------------
st.subheader("Chat with SmartKnowledge AI")

# Voice Input
audio_file = st.file_uploader("Upload voice to ask", type=["wav", "mp3", "opus"], key="voice_input_main")
user_question = None

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(audio_file.read())
        audio_path = f.name
    with st.spinner("Listening..."):
        text, lang = speech_to_text(audio_path)
        user_question = text
        st.success(f"Recognized ({lang}): {text}")
    os.remove(audio_path)

# Text Input
text_input = st.chat_input("Type your question here...")
if text_input:
    user_question = text_input

# ----------------- Chat Logic -----------------
if user_question:
    with st.chat_message("user"):
        st.write(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if is_greeting(user_question):
                answer = "Hi! How can I help you today?"
            elif st.session_state.pdf_index and use_pdf:
                answer = get_pdf_answer(
                    user_question,
                    st.session_state.pdf_index,
                    st.session_state.pdf_chunks,
                    generate_answer
                )
            else:
                answer = generate_answer(user_question, st.session_state.chat_history)

            st.write(answer)
            if voice_output:
                speak_text(answer)

    # Save chat
    st.session_state.chat_history.append((user_question, answer))
    st.session_state.chat_history = st.session_state.chat_history[-20:]
    save_chat(st.session_state.username, user_question, answer)

