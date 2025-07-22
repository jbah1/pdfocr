


# Tesseract PDF Processing Research

## Summary

Tesseract can process PDFs directly when the appropriate dependencies are installed. However, the current system doesn't have PDF support compiled in. As an alternative, we can use `pdftoppm` from poppler-utils to convert PDF pages to PNG images, then process those with Tesseract.

## Findings

### 1. Tesseract PDF Support

- Tesseract 5.3.0 is installed but lacks PDF reading support
- PDF reading requires Leptonica to be compiled with PDF support
- Alternative: Use `pdftoppm` to convert PDF to images first

### 2. Tesseract Output Formats

Tesseract supports multiple output formats that provide layout information:

1. **Plain text** (default): Just the extracted text
2. **hOCR**: HTML with bounding box information
3. **TSV**: Tab-separated values with coordinates
4. **PDF**: Searchable PDF output

### 3. Column Detection Approach

The TSV output provides word-level bounding boxes with:
- `left`, `top`, `width`, `height` coordinates
- `conf` - confidence score
- `text` - recognized text

This allows us to:
1. Group words by vertical position to detect lines
2. Group lines by horizontal position to detect columns
3. Extract text column by column

### 4. Page Segmentation Modes

Tesseract's `--psm` parameter controls page segmentation:
- `1`: Automatic page segmentation with OSD (best for our case)
- `4`: Assume a single column of text
- `6`: Assume a single uniform block of text

## Recommendations

### For Backend Implementation

1. **PDF to Image Conversion**: Use `pdftoppm` to convert PDF pages to PNG
2. **Tesseract Processing**: Process each PNG with Tesseract using:
   - Language: `-l nld` (Dutch)
   - Page segmentation: `--psm 1`
   - Output format: TSV for layout analysis
3. **Column Detection**: Parse TSV output to detect columns based on bounding boxes
4. **Markdown Generation**: Format extracted text by column into markdown

### Dependencies Needed

- `poppler-utils` (for `pdftoppm`)
- `tesseract-ocr` (with Dutch language support)
- `pytesseract` (Python wrapper)

### Advantages of This Approach

1. **No PyMuPDF dependency**: Uses only Tesseract and poppler-utils
2. **Better layout detection**: Tesseract's TSV output provides precise bounding boxes
3. **Language support**: Can handle Dutch text properly
4. **Future extensibility**: Can add more sophisticated layout analysis

## Next Steps

1. Update backend to use `pdftoppm` + Tesseract instead of PyMuPDF
2. Implement TSV parsing for column detection
3. Generate structured markdown from columnar text
4. Test with sample PDF and verify output quality

