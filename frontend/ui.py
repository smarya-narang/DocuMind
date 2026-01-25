import streamlit as st
import requests
import time

# 1. Setup Page Config
st.set_page_config(page_title="DocuMind AI", page_icon="🧠", layout="wide")

# 2. Inject Custom CSS (Aggressive White Text Mode)
st.markdown("""
    <style>
    /* --- GLOBAL TEXT RESET --- */
    /* Force all text in the app to be white */
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #FFFFFF !important;
    }
    
    /* --- BACKGROUNDS --- */
    .stApp {
        background-color: #0E1117; /* Deep Dark Blue-Black */
    }
    section[data-testid="stSidebar"] {
        background-color: #161B22; /* Slightly lighter sidebar */
        border-right: 1px solid #30363D;
    }
    
    /* --- INPUT FIELDS --- */
    /* Text Input Boxes */
    .stTextInput > div > div > input {
        background-color: #0D1117;
        color: #FFFFFF !important; /* Input text white */
        border: 1px solid #30363D;
        border-radius: 8px;
    }
    /* Placeholder text (the faint text) */
    ::placeholder {
        color: #8B949E !important; 
        opacity: 1; /* Firefox */
    }

    /* --- BUTTONS --- */
    /* Primary Action Button */
    .stButton > button {
        background: linear-gradient(90deg, #238636 0%, #2EA043 100%);
        color: white !important;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* --- CHAT BUBBLES --- */
    /* User Message (Right Side) */
    .user-card {
        background-color: #1F6FEB; /* Bright Blue */
        color: white !important;
        padding: 15px;
        border-radius: 15px 15px 5px 20px;
        margin-bottom: 10px;
        text-align: right;
        width: fit-content;
        margin-left: auto; /* Pushes to right */
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    /* AI Message (Left Side) */
    .ai-card {
        background-color: #21262D; /* Dark Gray */
        color: white !important;
        padding: 15px;
        border-radius: 15px 15px 20px 5px;
        margin-bottom: 10px;
        text-align: left;
        width: fit-content;
        margin-right: auto; /* Pushes to left */
        border: 1px solid #30363D;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    
    /* --- FILE UPLOADER --- */
    section[data-testid="stFileUploader"] {
        background-color: #0D1117;
        border: 1px dashed #30363D;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Session State (Chat Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Main Header
st.title("🧠 DocuMind")
st.markdown("### Enterprise-Grade RAG System")

# 5. Sidebar
with st.sidebar:
    st.header("📂 Document Center")
    uploaded_file = st.file_uploader("Upload Policy PDF", type="pdf")
    
    if uploaded_file:
        if st.button("🚀 Upload & Analyze"):
            with st.spinner("Processing neural embeddings..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    response = requests.post("http://127.0.0.1:8000/upload", files=files)
                    if response.status_code == 200:
                        st.success("✅ Document Indexed!")
                    else:
                        st.error("❌ Indexing Failed.")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 6. Display Chat History
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-card">👤 <b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-card">🤖 <b>DocuMind:</b><br>{message["content"]}</div>', unsafe_allow_html=True)

# 7. Chat Input Area
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input("Ask a question:", placeholder="e.g. What is the leave policy?", label_visibility="collapsed")
    with col2:
        submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Save User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Thinking..."):
        try:
            # Get AI Response
            response = requests.post("http://127.0.0.1:8000/query", data={"question": user_input})
            if response.status_code == 200:
                answer_text = response.json().get("relevant_context", "No context found.")
                
                # Save AI Message
                st.session_state.messages.append({"role": "ai", "content": answer_text})
                st.rerun()
            else:
                st.error("Backend Error.")
        except Exception as e:
            st.error(f"Error: {e}")