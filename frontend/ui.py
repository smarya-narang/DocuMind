import streamlit as st
import requests
import time

# 1. Setup Page Config
st.set_page_config(page_title="DocuMind AI", page_icon="🧠", layout="wide")

# 2. Styles: Royal Blue Theme + Browse Button Fix
st.markdown("""
    <style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* BACKGROUND: Deep Royal Blue Gradient */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        background-attachment: fixed;
    }

    /* SIDEBAR: Semi-transparent Dark Blue */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.2);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* GLOBAL TEXT: White */
    h1, h2, h3, p, div, span, label, small {
        color: #FFFFFF !important;
    }

    /* --- FILE UPLOADER FIX --- */
    [data-testid="stFileUploader"] {
        background-color: rgba(0, 0, 0, 0.3);
        border: 1px dashed rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 10px;
    }
    [data-testid="stFileUploader"] button {
        color: #00d2ff !important;
        border-color: #00d2ff !important;
        background-color: transparent !important;
    }
    /* ------------------------- */

    /* BUTTONS: Gradient */
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
    }

    /* INPUT BOX: Glassmorphism */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar
with st.sidebar:
    st.title("🧠 DocuMind")
    st.markdown("### Document Center")
    uploaded_file = st.file_uploader("Upload Policy PDF", type="pdf")
    
    if uploaded_file:
        if st.button("🚀 Upload & Analyze", use_container_width=True):
            with st.spinner("Processing neural embeddings..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    response = requests.post("http://127.0.0.1:8000/upload", files=files)
                    if response.status_code == 200:
                        st.success("✅ Document Indexed!")
                    else:
                        st.error("❌ Indexing Failed.")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. Main Chat Area
st.title("Chat with your Document")
st.markdown("_Enterprise-Grade RAG System_")

# Display History
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 6. Chat Input
if prompt := st.chat_input("Ask a question about your PDF..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner("Thinking..."):
            try:
                response = requests.post("http://127.0.0.1:8000/query", data={"question": prompt})
                if response.status_code == 200:
                    answer = response.json().get("relevant_context", "No context found.")
                    for chunk in answer.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                else:
                    message_placeholder.error("Backend Error.")
                    full_response = "Error."
            except Exception as e:
                message_placeholder.error(f"Connection Error: {e}")
                full_response = str(e)
    st.session_state.messages.append({"role": "assistant", "content": full_response})