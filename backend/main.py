"""
FastAPI backend for PDF Menu OCR to Markdown MVP
- Accepts PDF upload
- Extracts images from each page using PyMuPDF
- Runs OCR on each image using pytesseract
- Returns structured markdown (basic MVP: concatenated OCR text)
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pytesseract
import tempfile
import os
from pdf_processor import process_pdf_to_markdown

app = FastAPI(title="PDF Menu OCR to Markdown API", description="MVP for PDF to Markdown conversion with OCR", version="0.1.0")

# Allow CORS for local network
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    if file.size and file.size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 50MB).")
    try:
        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf.write(await file.read())
            temp_pdf_path = temp_pdf.name

        # Process PDF using Tesseract-based solution
        markdown = process_pdf_to_markdown(temp_pdf_path)

        # Clean up temporary file
        try:
            os.remove(temp_pdf_path)
        except:
            pass

        return {"markdown": markdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
