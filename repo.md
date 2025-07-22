
# PDF Menu OCR to Markdown Web Application

## Overview
This repository contains a web application that allows users to upload PDF menus, perform OCR (Optical Character Recognition) on the content, and output structured markdown files. The application is designed to handle menus with a consistent layout: a front page with recipe titles followed by detailed recipe pages.

## Project Structure

```
pdfocr/
├── backend/                # FastAPI backend for PDF processing
│   ├── README.md           # Backend documentation
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── venv/               # Python virtual environment
├── docs/                   # Documentation and sample files
│   ├── PRD.md              # Product Requirements Document
│   └── Wimpies-recept-kwartel--witlof--druif.pdf  # Sample menu PDF
└── repo.md                 # This file (repository overview)
```

## Key Features

- **PDF Upload**: Users can upload PDF files containing menu images
- **OCR Processing**: Uses Tesseract to extract text from PDF images
- **Structure Recognition**: Detects recipe titles, ingredients, steps, and substeps
- **Markdown Output**: Generates structured, editable markdown files
- **Modern Web UI**: Clean, responsive interface for file upload and editing

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 52560
   ```

### Sample PDF

A sample menu PDF is included in the `docs/` directory for testing:
- `2023-10 kwartel, kabeljauw, kalf, bananenrol.pdf`

## Development Roadmap

1. **MVP**: Basic PDF upload, OCR processing, and markdown output
2. **UI Polish**: Modern interface design and markdown editor
3. **Advanced Parsing**: Improved structure recognition and substep handling
4. **Deployment**: Production-ready deployment and documentation

## Documentation

- [Product Requirements Document (PRD)](docs/PRD.md)
- [Backend README](backend/README.md)
- [Tesseract Conversion Plan](docs/tesseract-conversion-plan.md)
- [Tesseract Research](docs/tesseract-research.md)
- [Tesseract Testing](docs/tesseract-testing.md)

## License

This project is licensed under the MIT License.
