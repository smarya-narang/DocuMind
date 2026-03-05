from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from pydantic import BaseModel
import shutil
import os
from typing import List, Dict, Any
=======
import shutil
import os
import csv
from datetime import datetime
>>>>>>> main
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

<<<<<<< HEAD
UPLOAD_DIR = "app/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- NEW: Define the structure for incoming questions ---
class QueryModel(BaseModel):
    question: str
    history: List[Dict[str, Any]] = []
=======
# Directories
UPLOAD_DIR = "app/data"
LOG_FILE = "app/data/query_logs.csv"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Log File with Headers if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Question", "Answer_Length"])

def log_interaction(question, answer):
    """Saves the Q&A interaction to a CSV file for analytics."""
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), question, len(answer)])
>>>>>>> main

@app.get("/")
def read_root():
    return {"status": "running", "message": "DocuMind Backend is Live!"}

<<<<<<< HEAD
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
=======
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Train the brain
    create_vector_db(file_path)
    return {"status": "success", "filename": file.filename, "message": "Brain updated!"}
>>>>>>> main

# --- UPGRADED: Now accepts JSON with history ---
@app.post("/query")
<<<<<<< HEAD
async def ask_question(payload: QueryModel):
    # Pass both the question and the history to the Brain
    context = query_vector_db(payload.question, payload.history)
    return {"question": payload.question, "relevant_context": context}
=======
async def ask_question(question: str = Form(...)):
    context = query_vector_db(question)
    
    # LOG THE DATA for Tableau
    log_interaction(question, context)
    
    return {"question": question, "relevant_context": context}
>>>>>>> main
