import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

# Path where the Brain (Vector Database) will be saved
DB_FAISS_PATH = "vectorstore/db_faiss"

def create_vector_db(pdf_path: str):
    """
    Ingests a PDF, splits text, creates embeddings, and saves to FAISS.
    """
    print(f"🧠 Learning from: {pdf_path}")
    
    # 1. Load the PDF
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found at {pdf_path}")
        return False
        
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        if not documents:
            print("❌ Error: No text could be extracted from this PDF.")
            return False
            
    except Exception as e:
        print(f"❌ Error loading PDF: {e}")
        return False

    # 2. Split Text (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    print(f"✂️  Split into {len(texts)} chunks.")

    # 3. Create Embeddings
    print("🧠 Generating Embeddings... (This may take a moment)")
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    # 4. Create and Save Vector Store
    try:
        db = FAISS.from_documents(texts, embeddings)
        db.save_local(DB_FAISS_PATH)
        print(f"💾 Vector Database saved to {DB_FAISS_PATH}")
        return True
    except Exception as e:
        print(f"❌ Error creating Vector DB: {e}")
        return False

def query_vector_db(query: str):
    """
    Searches the local FAISS database for the 3 most relevant chunks.
    """
    # 1. Check if DB exists
    if not os.path.exists(DB_FAISS_PATH):
        return "⚠️ System Error: No knowledge base found. Please upload a document first."
        
    # 2. Setup Embeddings
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    
    # 3. Load the DB
    try:
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        return f"❌ Error loading Brain: {e}"
    
    # 4. Perform Search
    try:
        results = db.similarity_search(query, k=3)
        if results:
            context = "\n\n---\n".join([doc.page_content for doc in results])
            return context
        else:
            return "No relevant information found."
    except Exception as e:
        return f"❌ Search Error: {e}"