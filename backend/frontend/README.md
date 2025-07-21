# PDF Menu OCR to Markdown Frontend (React)

## Overview
This React frontend allows users to upload a PDF menu, sends it to the backend for OCR processing, and displays the extracted markdown in an editable interface.

## Features
- File upload (PDF, max 50MB)
- Calls FastAPI backend at http://localhost:52560/upload
- Displays and allows editing of markdown using react-markdown

## Usage
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm start
   ```
3. Open http://localhost:3000 in your browser.

## Next Steps
- Improve markdown structure and formatting
- Add recipe/ingredient/step recognition
- UI/UX polish
