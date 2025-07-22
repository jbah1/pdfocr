

# Tesseract Conversion Plan

## Objective
Convert the PDF Menu OCR backend to use only Tesseract for both column recognition and OCR, removing the PyMuPDF dependency.

## Current Implementation Analysis

### Current Workflow
1. PDF upload via FastAPI endpoint
2. PyMuPDF extracts images from each PDF page
3. pytesseract performs OCR on each extracted image
4. Returns basic markdown with concatenated OCR text

### Current Dependencies
- `PyMuPDF` (fitz) - for PDF image extraction
- `pytesseract` - for OCR
- `Pillow` - for image handling

## Target Implementation

### New Workflow
1. PDF upload via FastAPI endpoint (unchanged)
2. Tesseract processes PDF directly with layout analysis
3. Extract text with column/structure information
4. Generate structured markdown

### Dependencies to Keep
- `pytesseract` - for OCR (with PDF support)
- Remove `PyMuPDF` and `Pillow` dependencies

## Implementation Plan

### Phase 1: Research and Setup
1. [ ] Research Tesseract's PDF processing capabilities
2. [ ] Test Tesseract's layout analysis modes (hOCR, TSV, etc.)
3. [ ] Determine best approach for column detection

### Phase 2: Backend Conversion
1. [ ] Update `main.py` to use Tesseract directly on PDF
2. [ ] Implement column detection using Tesseract output
3. [ ] Maintain same API interface and response format
4. [ ] Update requirements.txt to remove PyMuPDF/Pillow

### Phase 3: Testing
1. [ ] Create test cases for different PDF layouts
2. [ ] Test with sample PDF (Wimpies-recept-kwartel--witlof--druif.pdf)
3. [ ] Verify markdown output structure
4. [ ] Performance testing

### Phase 4: Documentation
1. [ ] Update README with new implementation details
2. [ ] Document Tesseract configuration and usage
3. [ ] Update PRD if needed

## Technical Considerations

### Tesseract PDF Processing
- Tesseract can process PDFs directly with `--oem 1` (LSTM OCR engine)
- Layout analysis available via hOCR, TSV, or PDF output formats
- Need to configure for Dutch language if needed

### Column Detection
- Use Tesseract's bounding box information to detect columns
- Analyze word/line positions to determine column structure
- May need post-processing to group text by column

### Markdown Structure
- Maintain current structure: `# Page N` headers with text content
- Future enhancement: structured recipe format

## Test Plan

### Test Cases
1. **Basic PDF Processing**: Verify Tesseract can process PDF directly
2. **Column Detection**: Test column recognition on sample PDF
3. **Text Extraction**: Verify accurate OCR text extraction
4. **Markdown Output**: Ensure proper markdown formatting
5. **Performance**: Test processing time for multi-page PDFs

### Test Files
- Use existing sample: `docs/2023-10 kwartel, kabeljauw, kalf, bananenrol.pdf`
- Create additional test PDFs with different column layouts

### Expected Output Format
For page-2.png analysis, the desired output should be:

```
November 2023
Voorgerecht
hazenrug filet met kool salade en rode biet
Ingredienten voor 10 personen

# First column:
Hazenrug filet;
4 hazenrug filet
Peper zout olijfolie
6 grote champignons 2 sjalot. 1/4
bieslook

# Second column:
Garnituur:
1/2 spitskool
1/4 rode kool
Tijm peper zout, azijn
suiker
Bieten peper zout olijfolie

# Third column:
Dressing:
50 gr rode wijn azijn,
2 sjalotjes, 100 gr
zonnebloem olie, peper, zout
```

For page-.3png analysis, the desired output should be:

```
November 2023
Tussengerecht
rood poot patrijs met witlof, uit en ananas
Ingredienten voor 10 personen

# First column:
Patrijs met rode pootjes:
5 x patrijs
Peper, zout
Fond 2 bakjes, 1 bakje water

# Second column:
Garnituur:
Witlof 8/10 stronkjes
Peper, zout, honing
4 aardappels
3 witte uien, 2 dl rode wijn
azijn, 2/4 lepels suiker

# Third column:
Ananas saus:
2 bakjes fond 1/4 ananas
Peper, zout
```

For page-4.png analysis, the desired output should be:

```
November 2023
Hoofdgerecht
Hertenhaas met orzo risotto
Ingredienten voor 10 personen

# First column:
Hertenhaas filet:
2 filets
peper, zout, olijfolie

# Second column:
Groenten:


# Third column:
Dressing:
50 gr rode wijn azijn,
2 sjalotjes, 100 gr
zonnebloem olie, peper, zout
```

For page-2.png analysis, the desired output should be:

```
November 2023
Voorgerecht
hazenrug filet met kool salade en rode biet
Ingredienten voor 10 personen

# First column:
Hazenrug filet;
4 hazenrug filet
Peper zout olijfolie
6 grote champignons 2 sjalot. 1/4
bieslook

# Second column:
Garnituur:
1/2 spitskool
1/4 rode kool
Tijm peper zout, azijn
suiker
Bieten peper zout olijfolie

# Third column:
Dressing:
50 gr rode wijn azijn,
2 sjalotjes, 100 gr
zonnebloem olie, peper, zout
```

## Risks and Mitigations

### Risks
1. Tesseract's PDF processing may not be as reliable as image-based OCR
2. Column detection may be less accurate than dedicated layout analysis tools
3. Performance may be impacted by processing large PDFs directly

### Mitigations
1. Test thoroughly with sample PDFs
2. Implement fallback mechanisms if needed
3. Optimize Tesseract configuration for performance

## Timeline

1. **Day 1-2**: Research and initial testing
2. **Day 3-4**: Backend implementation
3. **Day 5**: Testing and debugging
4. **Day 6**: Documentation and final review

