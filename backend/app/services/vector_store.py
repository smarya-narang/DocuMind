import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
# NOTICE: We use the updated import for embeddings to avoid warnings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.services.pdf_loader import load_pdf_text

# Define where the database will be saved
DB_FAISS_PATH = "vectorstore/db_faiss"

def create_vector_db(pdf_path: str):
    """
    Ingests a PDF, splits text, creates embeddings, and saves to FAISS.
    Returns True if successful, False otherwise.
    """
    print(f"📄 Loading PDF from: {pdf_path}")
    
    # 1. Load Text
    raw_text = load_pdf_text(pdf_path)
    if not raw_text:
        print("❌ Error: No text found in PDF.")
        return False

    # 2. Split Text (Chunks)
    # We split by 500 characters with 50 overlap to keep context
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(raw_text)
    print(f"✂️  Split into {len(texts)} chunks.")

    # 3. Create Embeddings
    print("🧠 Generating Embeddings... (This may take a moment)")
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    # 4. Create Vector Store
    try:
        db = FAISS.from_texts(texts, embeddings)
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
        
    # 2. Setup Embeddings (Same model as creation)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    
    # 3. Load the DB
    # allow_dangerous_deserialization=True is safe here because WE created the file locally
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    
    # 4. Perform Search (Top 3 results)
    results = db.similarity_search(query, k=3)
    
    # 5. Format results into a single string
    if results:
        context = "\n\n---\n".join([doc.page_content for doc in results])
        return context
    else:
        return "No relevant information found."

# --- TEST BLOCK (Run this file directly to test) ---
if __name__ == "__main__":
    # Test Data Creation
    test_pdf = "../data/sample_policy.pdf"
    if os.path.exists(test_pdf):
        create_vector_db(test_pdf)
    
    # Test Search
    test_query = "What is the leave policy?"
    answer = query_vector_db(test_query)
    print(f"\n🔍 Query: {test_query}")
    print(f"💡 Result:\n{answer}")