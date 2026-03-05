from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from typing import List, Dict, Any
from app.services.vector_store import create_vector_db, query_vector_db

app = FastAPI()

# Allow Frontend to talk to Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "app/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- NEW: Define the structure for incoming questions ---
class QueryModel(BaseModel):
    question: str
    history: List[Dict[str, Any]] = []

@app.get("/")
def read_root():
    return {"status": "running", "message": "DocuMind Backend is Live!"}

@app.post("/upload_multiple")
async def upload_multiple_documents(files: List[UploadFile] = File(...)):
    saved_file_paths = []
    
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_file_paths.append(file_path)
    
    create_vector_db(saved_file_paths)
    
    return {
        "status": "success", 
        "filenames": [file.filename for file in files], 
        "message": f"Brain updated with {len(files)} documents!"
    }

# --- UPGRADED: Now accepts JSON with history ---
@app.post("/query")
async def ask_question(payload: QueryModel):
    # Pass both the question and the history to the Brain
    context = query_vector_db(payload.question, payload.history)
    return {"question": payload.question, "relevant_context": context}
