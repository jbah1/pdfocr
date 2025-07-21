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
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

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
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        markdown_pages = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))
            text = pytesseract.image_to_string(image)
            markdown_pages.append(f"# Page {page_num+1}\n\n{text}\n")
        markdown = "\n---\n".join(markdown_pages)
        return {"markdown": markdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
