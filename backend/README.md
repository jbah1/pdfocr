# PDF Menu OCR to Markdown Backend (FastAPI)

## Overview
This FastAPI backend provides an endpoint to upload a PDF menu, extract images from each page, perform OCR using Tesseract, and return the extracted text as markdown.

## Features
- Accepts PDF uploads (max 50MB)
- Extracts images from each page using PyMuPDF
- Runs OCR on each image using pytesseract
- Returns concatenated markdown (MVP)
- CORS enabled for local network

## Usage
1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 52560
   ```
3. POST a PDF to `/upload` endpoint. Response is `{ "markdown": ... }`.

## Next Steps
- Add structure recognition for recipes, ingredients, steps, and substeps
- Improve markdown formatting
- Integrate with frontend
