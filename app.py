import streamlit as st
import requests

# -----------------------------
# CONFIG
# -----------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"

# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------
st.sidebar.title("⚙️ Settings")

MODEL_NAME = st.sidebar.selectbox(
    "Choose Model",
    ["llama3", "mistral"]
)

if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.history = []
    st.rerun()

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("💬 Local LLM Chat App")

# -----------------------------
# DISPLAY CHAT HISTORY (Chat UI)
# -----------------------------
for chat in st.session_state.history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["bot"])

# -----------------------------
# BUILD CONTEXT PROMPT
# -----------------------------
def build_prompt():
    prompt = ""
    for chat in st.session_state.history:
        prompt += f"User: {chat['user']}\nAssistant: {chat['bot']}\n"
    return prompt

# -----------------------------
# FUNCTION TO CALL OLLAMA
# -----------------------------
def query_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------------
# USER INPUT (Chat Input)
# -----------------------------
user_input = st.chat_input("Ask something...")

# -----------------------------
# HANDLE INPUT
# -----------------------------
if user_input:
    # Show user message instantly
    with st.chat_message("user"):
        st.write(user_input)

    # Build full conversation context
    full_prompt = build_prompt() + f"User: {user_input}\nAssistant:"

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_ollama(full_prompt)

            if "Error" in response:
                st.error(response)
            else:
                st.write(response)

    # Save to history
    st.session_state.history.append({
        "user": user_input,
        "bot": response
    })
