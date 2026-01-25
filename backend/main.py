import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from app.services.vector_store import create_vector_db, query_vector_db

# Initialize the App
app = FastAPI(title="DocuMind API", version="1.0")

@app.get("/")
async def health_check():
    """Simple check to see if the server is running."""
    return {"status": "running", "message": "DocuMind Backend is Live!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF. 
    It saves the file and instantly triggers the AI training (Vector DB creation).
    """
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    file_location = f"data/{file.filename}"
    
    # 1. Save the file to disk
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. Trigger the "Brain" to read and learn it
    success = create_vector_db(file_location)
    
    if success:
        return {"status": "success", "filename": file.filename, "message": "File processed and indexed successfully."}
    else:
        return {"status": "error", "message": "Failed to process the PDF."}

@app.post("/query")
async def ask_question(question: str = Form(...)):
    """
    Endpoint to ask a question.
    It searches the Vector DB and returns the relevant text chunks.
    """
    # 1. Search the database
    context = query_vector_db(question)
    
    return {"question": question, "relevant_context": context}

if __name__ == "__main__":
    import uvicorn
    # Run the server on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)