


# Tesseract Testing Documentation

## Purpose
Track the testing process for converting the PDF OCR backend to use only Tesseract for both column recognition and OCR.

## Test Environment

- **System**: Ubuntu LXC (Proxmox)
- **Tesseract Version**: 5.3.0
- **Python Version**: 3.x
- **Sample PDF**: `docs/2023-10 kwartel, kabeljauw, kalf, bananenrol.pdf`

## Test Cases

### Test Case 1: Basic PDF Processing

**Objective**: Verify Tesseract can process PDF directly and extract text.

**Steps**:
1. Install Tesseract with PDF support
2. Test basic PDF processing command:
   ```bash
   tesseract input.pdf stdout -l nld
   ```
3. Verify text output matches expected content

**Expected Result**: Text extraction should be comparable to current PyMuPDF + pytesseract approach.

**Status**: [Pending]

### Test Case 2: Layout Analysis with hOCR

**Objective**: Extract structured layout information using Tesseract's hOCR output.

**Steps**:
1. Run Tesseract with hOCR output:
   ```bash
   tesseract input.pdf stdout -l nld hocr
   ```
2. Parse hOCR output to extract bounding boxes and text
3. Analyze word/line positions to detect columns

**Expected Result**: Should get structured data with word positions for column detection.

**Status**: [Pending]

### Test Case 3: Column Detection Algorithm

**Objective**: Implement and test column detection using Tesseract output.

**Steps**:
1. Process hOCR or TSV output to get word bounding boxes
2. Group words by vertical position to detect lines
3. Group lines by horizontal position to detect columns
4. Test with sample PDF

**Expected Result**: Accurate column detection (3 columns for ingredients).

**Status**: [Pending]

### Test Case 4: Markdown Generation

**Objective**: Generate proper markdown from structured Tesseract output.

**Steps**:
1. Process Tesseract output to extract text by column
2. Format as markdown with appropriate headers
3. Compare output with current implementation

**Expected Result**: Markdown should be structured and readable.

**Status**: [Pending]

### Test Case 5: Performance Testing

**Objective**: Measure processing time for multi-page PDFs.

**Steps**:
1. Process sample PDF (5 pages) with Tesseract
2. Measure total processing time
3. Compare with current PyMuPDF + pytesseract approach

**Expected Result**: Processing time should be reasonable (< 30 seconds for 5-page PDF).

**Status**: [Pending]

## Test Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| Basic PDF Processing | ✅ Completed | Tesseract works with PDF->PNG conversion |
| Layout Analysis with hOCR | ✅ Completed | hOCR output provides bounding boxes |
| Layout Analysis with TSV | ✅ Completed | TSV output provides precise coordinates |
| Column Detection Algorithm | ✅ Completed | Analyzed x-coordinate distribution for column boundaries |
| Markdown Generation | Pending | Need to implement formatting |
| Performance Testing | Pending | Need to test full pipeline |

## Issues and Resolutions

| Issue | Resolution | Status |
|-------|------------|--------|
| None yet | N/A | |

## Next Steps

1. Set up Tesseract with PDF support
2. Run initial PDF processing tests
3. Implement and test hOCR parsing
4. Develop column detection algorithm
5. Integrate with FastAPI backend

