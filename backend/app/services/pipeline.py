from app.services.pdf_loader import load_pdf_text
from app.services.vector_store import create_vector_db
from langchain.text_splitter import RecursiveCharacterTextSplitter

def build_knowledge_base(pdf_path):
    print(f"📂 Loading PDF: {pdf_path}")
    
    # 1. Load Text
    raw_text = load_pdf_text(pdf_path)
    
    # 2. Split Text (AI needs small chunks, not whole books)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(raw_text)
    print(f"✂️ Split document into {len(chunks)} chunks.")
    
    # 3. Vectorize
    create_vector_db(chunks)

if __name__ == "__main__":
    # Test with your sample PDF
    # Note: Path assumes you are running from 'backend/' folder
    test_pdf = "../data/sample_policy.pdf"
    
    try:
        build_knowledge_base(test_pdf)
    except Exception as e:
        print(e)