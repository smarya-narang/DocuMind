import streamlit as st
import requests
import time
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# 1. Setup Page Config
st.set_page_config(page_title="DocuMind AI", page_icon="🧠", layout="wide")

# 2. Styles: Premium Dark Theme + Glassmorphism
st.markdown("""
    <style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* Hide Streamlit Defaults */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}

    /* Premium Dark Mesh Gradient Background */
    .stApp {
        background: radial-gradient(circle at 15% 50%, rgba(138,43,226,0.08), transparent 40%),
                    radial-gradient(circle at 85% 30%, rgba(65,105,225,0.08), transparent 40%),
                    #050508;
        background-attachment: fixed;
    }

    /* SIDEBAR: Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 15, 0.4) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* GLOBAL TEXT: White */
    h1, h2, h3, p, div, span, label, small {
        color: #f8f8fa !important;
    }

    /* --- FILE UPLOADER PREMIUM FIX --- */
    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.02);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 16px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #8a2be2;
        background-color: rgba(255, 255, 255, 0.04);
    }

    [data-testid="stFileUploader"] button {
        color: #fff !important;          
        border: none !important;
        background: linear-gradient(135deg, #8a2be2, #4169e1) !important; 
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(138,43,226,0.4) !important;
    }

    /* MAIN BUTTONS: Gradient */
    .stButton > button {
        background: linear-gradient(135deg, #8a2be2, #4169e1);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(138,43,226,0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(138,43,226,0.4);
    }

    /* INPUT BOX: Glassmorphism */
    .stTextInput > div > div > input, .stChatInputContainer > div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }

    .stTextInput > div > div > input:focus, .stChatInputContainer > div:focus-within {
        border-color: #8a2be2 !important;
        box-shadow: 0 0 0 2px rgba(138,43,226,0.2) !important;
    }
    
    /* CHAT BUBBLES: Glassmorphism */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1rem;
    }
    
    /* TITLE GRADIENT */
    h1 {
        background: linear-gradient(135deg, #b070ff, #7090ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar (UPGRADED FOR MULTIPLE FILES)
with st.sidebar:
    st.title("🧠 DocuMind")
    st.markdown("### Document Center")
    
    uploaded_files = st.file_uploader("Upload Policy PDFs", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🚀 Upload & Analyze", use_container_width=True):
            with st.spinner("Processing neural embeddings..."):
                files_to_send = [("files", (file.name, file, "application/pdf")) for file in uploaded_files]
                
                try:
                    response = requests.post(f"{BACKEND_URL}/upload_multiple", files=files_to_send)
                    
                    if response.status_code == 200:
                        st.success(f"✅ {len(uploaded_files)} Document(s) Indexed!")
                    else:
                        st.error("❌ Indexing Failed. Backend might not be updated yet.")
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
if prompt := st.chat_input("Ask a question about your PDF(s)..."):
    
    # A. User Message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # B. AI Response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/query", 
                    json={
                        "question": prompt, 
                        "history": st.session_state.messages[:-1]
                    }
                )
                
                if response.status_code == 200:
                    answer = response.json().get("relevant_context", "No context found.")
                    
                    # Streaming effect
                    for chunk in answer.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                else:
                    message_placeholder.error(f"Backend Error: {response.status_code}")
                    full_response = "Error."
            except Exception as e:
                message_placeholder.error(f"Connection Error: {e}")
                full_response = str(e)
                
    st.session_state.messages.append({"role": "assistant", "content": full_response})