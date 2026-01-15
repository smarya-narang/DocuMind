import os
from pypdf import PdfReader

def load_pdf_text(file_path: str) -> str:
    """
    Reads a PDF file from the given path and returns its content as a string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")

    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        print(f"✅ Successfully loaded {len(reader.pages)} pages.")
        return text

    except Exception as e:
        raise Exception(f"❌ Failed to read PDF: {e}")

# --- TEST BLOCK ---
if __name__ == "__main__":
    # Test with a sample file in data/ folder
    test_path = test_path = "../data/sample_policy.pdf"
    try:
        content = load_pdf_text(test_path)
        print("\n--- TEXT PREVIEW ---")
        print(content[:200]) 
    except Exception as e:
        print(e)