
# Tesseract PSM Mode Comparison Analysis

## Summary

This analysis compares Tesseract PSM (Page Segmentation Mode) 6, 11, 12, and 13 for column detection and OCR accuracy on the sample PDF pages.

## Key Findings

1. **PSM 13** produces minimal output (6 lines) with no word-level data - not suitable for our needs
2. **PSM 6, 11, and 12** all produce word-level data (level 5 entries)
3. PSM 11 and 12 produce more total lines than PSM 6, suggesting more detailed layout analysis
4. All modes (6, 11, 12) show similar word-level entry counts, indicating comparable OCR performance

## Detailed Results

### Page 1
- PSM 6: 60 lines, 2 word entries
- PSM 11: 92 lines, 2 word entries
- PSM 12: 92 lines, 2 word entries
- PSM 13: 6 lines, 0 word entries (minimal output)

### Page 2
- PSM 6: 346 lines, 26 word entries
- PSM 11: 593 lines, 22 word entries
- PSM 12: 598 lines, 22 word entries
- PSM 13: 6 lines, 0 word entries (minimal output)

### Page 3
- PSM 6: 316 lines, 25 word entries
- PSM 11: 521 lines, 19 word entries
- PSM 12: 526 lines, 19 word entries
- PSM 13: 6 lines, 0 word entries (minimal output)

### Page 4
- PSM 6: 348 lines, 29 word entries
- PSM 11: 582 lines, 32 word entries
- PSM 12: 559 lines, 32 word entries
- PSM 13: 6 lines, 0 word entries (minimal output)

### Page 5
- PSM 6: 341 lines, 29 word entries
- PSM 11: 574 lines, 24 word entries
- PSM 12: 579 lines, 24 word entries
- PSM 13: 6 lines, 0 word entries (minimal output)

## Recommendations

1. **Avoid PSM 13** - Produces minimal output without word-level data
2. **PSM 11 and 12** produce more detailed layout information than PSM 6
3. **PSM 11** (Sparse text) and **PSM 12** (Sparse text with OCR) show similar performance
4. **PSM 6** (Assume uniform block of text) is currently working but may be less optimal for column detection

## Next Steps

1. Test PSM 11 and 12 with the current parsing logic
2. Evaluate which mode provides the best column detection
3. Consider using PSM 11 or 12 if they provide better column separation
4. Update the backend to use the optimal PSM mode

## Raw Data Files

All raw TSV output files are available in the `psm_comparison/` directory:
- `page-{N}-psm{M}.tsv` files contain the raw Tesseract output
- Files can be analyzed to understand the detailed differences between modes
