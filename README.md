# 🧠 DocuMind: Enterprise RAG System

<div align="center">
  <p>A secure, containerized Document Retrieval System utilizing Retrieval Augmented Generation (RAG) to chat intelligently with your PDFs.</p>
  
  [![Live Demo](https://img.shields.io/badge/Live_Frontend_Demo-050508?style=for-the-badge&logo=streamlit&logoColor=white)](https://documind-frontend-ywbn.onrender.com/)
  [![Backend API](https://img.shields.io/badge/Backend_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://documind-backend-u1mr.onrender.com/)
</div>

---

## 🌟 Overview
Built as a Semester 6 Capstone Project, DocuMind allows users to upload multiple PDF documents and perform semantic searches and AI-driven queries against them. The system embeds the text into a FAISS vector database and uses an LLM via LangChain to generate accurate, context-aware answers.

### ✨ Key Features
- **Intelligent Semantic Search**: Powered by `sentence-transformers` to find exact context across hundreds of pages.
- **Premium Glassmorphism UI**: A custom-styled Streamlit frontend featuring mesh gradients, frosted glass chat bubbles, and modern typography (Outfit/Inter).
- **FastAPI Backend**: A highly performant, fully decoupled Python backend handling embedding, retrieval, and LLM communication.
- **Fully Containerized**: Uses Docker and Docker Compose for seamless local development and easy cloud deployment.

---

## 🛠 Tech Stack

| Component | Technology |
| --- | --- |
| **Frontend** | Streamlit, Custom CSS Injection |
| **Backend** | FastAPI, Python 3.10 |
| **AI Engine** | LangChain, HuggingFace (`sentence-transformers`), Groq API |
| **Vector DB** | FAISS (Facebook AI Similarity Search) |
| **Deployment** | Docker, Docker Compose, Render (via `render.yaml` Blueprint) |

---

## 🚀 Live Demo
You can try out the live application hosted on Render here:
👉 **[DocuMind Frontend UI](https://documind-frontend-ywbn.onrender.com/)**

*(Note: The live demo runs on a free ephemeral tier. Uploaded PDFs and the vector database will reset when the server spins down. To persist your database indefinitely, run the project locally!)*

The Backend API Swagger documentation is automatically generated and accessible here:
👉 **[DocuMind API Docs](https://documind-backend-u1mr.onrender.com/docs)**

---

## 💻 Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/smarya-narang/DocuMind.git
   cd DocuMind
   ```

2. **Set your Environment Variables:**
   Create a `.env` file inside the `backend/` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   * The frontend will be instantly available at `http://localhost:8501`.
   * The backend will be available at `http://localhost:8000`.

---
<div align="center">
  <p>Built with ❤️ by Smarya Narang for Semester 6 Capstone</p>
</div>