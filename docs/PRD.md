# Product Requirements Document (PRD)

## Project: PDF Menu OCR to Markdown Web Application

### Sample Menu PDF
A sample menu PDF is included for reference and testing:

- **docs/Wimpies-recept-kwartel--witlof--druif.pdf**
  - This file is a real menu scan matching the target structure (front page + 4 recipe pages, columns of ingredients, steps/substeps).
  - Use this file for development, testing, and documentation examples.

### Overview
A modern web application that allows users to upload a PDF file containing images of a menu (with recipes), performs OCR (using the latest Tesseract), and outputs a structured, editable markdown file. The application is designed for menus with a consistent layout: a front page with 4 recipe titles, followed by 4 pages each describing a recipe. Each recipe page contains 3 columns of ingredients at the top and 3-5 steps (with possible substeps) below.

---

## Goals
- Enable users to upload a PDF menu and receive a structured markdown file as output.
- Use OCR to extract text from menu images, preserving structure (titles, ingredients, steps, substeps).
- Provide a modern, user-friendly web interface.
- Output markdown should be easily editable by the user.

---

## User Stories
1. **As a user, I want to upload a PDF menu so that I can digitize its contents.**
2. **As a user, I want the application to extract and structure the menu content into markdown, so I can edit and reuse it.**
3. **As a user, I want the markdown output to reflect the menu's structure: recipe titles, ingredients (in columns), steps, and substeps.**
4. **As a user, I want a modern, intuitive interface for uploading files and editing markdown.**

---

## Functional Requirements
- **PDF Upload:**
  - Users can upload a PDF file (containing images of menu pages).
- **OCR Processing:**
  - Use the latest Tesseract OCR engine to extract text from PDF images.
  - Support for multi-page PDFs.
- **Menu Structure Recognition:**
  - Detect and extract:
    - Front page with 4 recipe titles
    - 4 recipe pages, each with:
      - 3 columns of ingredients at the top
      - 3-5 steps below, each possibly with substeps
- **Markdown Generation:**
  - Output a markdown file with structured content:
    - Recipe titles as headers
    - Ingredients as lists (grouped by columns)
    - Steps and substeps as ordered/unordered lists
- **Markdown Editor:**
  - Display the generated markdown in an editable field (WYSIWYG or code editor)
  - Allow user to copy/download the markdown
- **Modern Web UI:**
  - Responsive, clean design using a modern framework (React, Vue, Svelte, etc.)

---

## Non-Functional Requirements
- **Performance:**
  - OCR and markdown generation should complete within a reasonable time for 5-page PDFs.
- **Security:**
  - Uploaded files are processed securely and not stored longer than necessary.
- **Browser Compatibility:**
  - Support for latest versions of Chrome, Firefox, Safari, Edge.
- **Accessibility:**
  - Basic accessibility for file upload and markdown editing.

---

## Clarifications (2025-07-21)
1. **Menu Layout Variations:** Menus will generally have the same structure (front page + 4 recipe pages), but the number of ingredient columns may differ. All other aspects remain the same.
2. **Substep Formatting:** Each menu should list ingredients per column (with a header per step if present). Steps and substeps should be represented as step + substeps, step + substeps, etc. Substeps can be nested lists in markdown.
3. **Image Retention:** Only text should be extracted and included in the markdown output. No images are required.
4. **Authentication:** No authentication is required; the tool is for local use only.
5. **File Size Limits:** Maximum PDF size supported is 50 MB.
6. **Deployment:** The application will run on a local Proxmox Ubuntu LXC and should be accessible from the local network.
7. **Branding/Styling:** No branding or color scheme preferences. The UI should be clean and simple.

---

## Suggested Tech Stack
- **Frontend:** React, Vue, or Svelte (with a modern UI library)
- **Backend:** Node.js (Express, Fastify) or Python (FastAPI, Flask)
- **OCR:** Tesseract (latest version, via tesseract.js or Python bindings)
- **PDF Processing:** pdf.js (frontend) or PyMuPDF/pdfminer (backend)

---

## Milestones
1. **MVP:** PDF upload, OCR, markdown output (basic structure)
2. **UI Polish:** Modern design, markdown editor
3. **Advanced Parsing:** Improved structure recognition, substep handling
4. **Deployment & Docs:** Production deployment, user documentation

---

## Next Steps
- Clarify open questions with stakeholders
- Finalize tech stack and architecture
- Begin implementation (MVP)
