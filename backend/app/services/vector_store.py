import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from groq import Groq

# --- CONFIGURE YOUR LLM HERE ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# -------------------------------
# -------------------------------

DB_FAISS_PATH = "vectorstore/db_faiss"

def create_vector_db(pdf_paths: list):
    print(f"🧠 Learning from {len(pdf_paths)} files...")
    all_documents = []
    
    for path in pdf_paths:
        if os.path.exists(path):
            try:
                loader = PyPDFLoader(path)
                docs = loader.load()
                all_documents.extend(docs)
                # --- NEW DEBUG LINE ---
                print(f"📄 Successfully read {path}. Extracted {len(docs)} pages.")
                # -----------------------
            except Exception as e:
                print(f"❌ Error loading {path}: {e}")
        else:
            print(f"⚠️ Warning: File not found at {path}")

    if not all_documents:
        print("❌ Error: No text could be extracted.")
        return False

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(all_documents)
    
    # --- NEW DEBUG LINE ---
    print(f"✂️  Combined and split into {len(texts)} chunks.")
    for i, t in enumerate(texts[:5]): # Print first 5 chunks to see if they contain course names
        print(f"   Chunk {i}: {t.page_content[:50]}...") 
    # -----------------------

    # ... rest of your function (embeddings and saving) ...
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    try:
        db = FAISS.from_documents(texts, embeddings)
        db.save_local(DB_FAISS_PATH)
        return True
    except Exception as e:
        return False

# --- UPGRADED: Added the history parameter ---
def query_vector_db(query: str, history: list = []):
    if not os.path.exists(DB_FAISS_PATH):
        return "⚠️ System Error: No knowledge base found. Please upload a document first."
        
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    
    try:
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        return f"❌ Error loading Brain: {e}"
    
    try:
        results = db.similarity_search(query, k=4)
        
        if not results:
            return "No relevant information found in the documents."
            
        context = "\n\n---\n".join([doc.page_content for doc in results])
        
        # Format the chat history into a readable script for the AI
        history_text = ""
        # We only take the last 4 messages so we don't overload the AI's token limit
        for msg in history[-4:]: 
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
        
        client = Groq(api_key=GROQ_API_KEY)
        
        # Added the Chat History to the prompt!
        prompt = f"""
        You are an intelligent assistant. Answer the user's question based ONLY on the provided context. 
        Keep your answer clear, concise, and conversational. Do not make up information.
        Use the Chat History to understand pronouns or context from previous questions.

        Chat History:
        {history_text}

        Context from Documents:
        {context}

        Current Question:
        {query}
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3, 
        )
        
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"🚨 GROQ'S EXACT ERROR: {str(e)}"
