from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import csv
from datetime import datetime
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

@app.get("/")
def read_root():
    return {"status": "running", "message": "DocuMind Backend is Live!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Train the brain
    create_vector_db(file_path)
    return {"status": "success", "filename": file.filename, "message": "Brain updated!"}

@app.post("/query")
async def ask_question(question: str = Form(...)):
    context = query_vector_db(question)
    
    # LOG THE DATA for Tableau
    log_interaction(question, context)
    
    return {"question": question, "relevant_context": context}