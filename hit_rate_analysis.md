



# Hit Rate Analysis

## Summary

This analysis compares the actual OCR results with the expected output from the conversion plan to understand what content is being detected vs. what is expected.

## Key Findings

1. **Extremely low hit rates**: Most pages have 0% hit rate for expected content
2. **Best performance**: PSM 6 shows slightly better results than PSM 11/12
3. **Page 5 shows highest hit rates**: Up to 23% for some columns
4. **Overall poor performance**: The current OCR approach is not detecting the expected ingredient content

## Detailed Results

### Page 2
- **PSM 6**: 0-7% hit rate across columns
- **PSM 11**: 0-7% hit rate across columns
- **PSM 12**: 0-7% hit rate across columns

### Page 3
- **PSM 6**: 0-14% hit rate across columns
- **PSM 11**: 0-7% hit rate across columns
- **PSM 12**: 0-7% hit rate across columns

### Page 4
- **PSM 6**: 0-7% hit rate across columns
- **PSM 11**: 0-14% hit rate across columns
- **PSM 12**: 0-14% hit rate across columns

### Page 5
- **PSM 6**: 14-23% hit rate across columns
- **PSM 11**: 10-23% hit rate across columns
- **PSM 12**: 10-23% hit rate across columns

## Issues Identified

1. **OCR not detecting expected content**: The Tesseract OCR is not recognizing the ingredient text
2. **Language detection issue**: May need Dutch language support
3. **Image quality**: The extracted images may not be clear enough
4. **Layout complexity**: The column layout may be confusing the OCR engine

## Recommendations

1. **Add Dutch language support**: Use `-l nld` parameter for Tesseract
2. **Improve image preprocessing**: Enhance image quality before OCR
3. **Test with different PSM modes**: Try PSM 4 (single column) or PSM 3 (fully automatic)
4. **Use OCR with layout analysis**: Try hOCR output format for better structure detection
5. **Post-process OCR results**: Apply text normalization and correction

## Next Steps

1. Test with Dutch language support
2. Implement image preprocessing
3. Test different PSM modes and OCR configurations
4. Analyze the actual content being detected to understand the mismatch

## Files

- `hit_rate_analysis/hit_rate_summary.md`: Summary of hit rate analysis
- `hit_rate_analysis/detailed_results.json`: Detailed analysis results with expected vs actual content

## Conclusion

The current OCR approach is not detecting the expected ingredient content. Significant improvements are needed to achieve the desired output format from the conversion plan.


