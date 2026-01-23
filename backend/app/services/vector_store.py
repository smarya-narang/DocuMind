import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Setup the Embedding Model (We use a free, local model)
# "all-MiniLM-L6-v2" is fast and standard for laptops.
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_vector_db(text_chunks):
    """
    Takes a list of text strings, converts them to vectors, 
    and saves them to a local FAISS index.
    """
    try:
        print("🔄 Generating embeddings... (This may take a moment)")
        
        # 2. Create the Vector Store
        vector_db = FAISS.from_texts(
            texts=text_chunks, 
            embedding=embedding_model
        )
        
        # 3. Save it locally so we don't have to rebuild it every time
        save_path = "faiss_index"
        vector_db.save_local(save_path)
        
        print(f"✅ Vector Database saved to '{save_path}'")
        return vector_db
        
    except Exception as e:
        raise Exception(f"❌ Failed to create Vector DB: {e}")

# --- TEST BLOCK ---
if __name__ == "__main__":
    # Fake data to test the logic
    sample_text = ["The semester fee is $5000.", "The exam starts at 9 AM."]
    
    try:
        db = create_vector_db(sample_text)
        
        # Quick Search Test
        query = "How much is the fee?"
        docs = db.similarity_search(query)
        print(f"\n🔍 Query: '{query}'")
        print(f"💡 Best Match: '{docs[0].page_content}'")
        
    except Exception as e:
        print(e)