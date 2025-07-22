





# hOCR Hit Rate Analysis

## Summary

This analysis compares hOCR output against expected content to determine if it improves hit rates over TSV output.

## Key Findings

1. **Significant improvement**: hOCR shows much better hit rates than TSV output
2. **Best performance**: PSM 6 and 12 perform similarly, with PSM 11 close behind
3. **Page 4 shows best results**: Up to 78% hit rate for column 3
4. **Consistent improvement**: All pages show 25-60% hit rates, much better than previous 0-23%

## Detailed Results

### Page 2
- **PSM 6**: 28-53% hit rate across columns (best: 53% for column 3)
- **PSM 11**: 35-53% hit rate across columns
- **PSM 12**: 35-53% hit rate across columns

### Page 3
- **PSM 6**: 25-37% hit rate across columns
- **PSM 11**: 25-37% hit rate across columns
- **PSM 12**: 25-37% hit rate across columns

### Page 4
- **PSM 6**: 25-78% hit rate across columns (best: 78% for column 3)
- **PSM 11**: 18-64% hit rate across columns
- **PSM 12**: 18-64% hit rate across columns

### Page 5
- **PSM 6**: 28-61% hit rate across columns (best: 61% for column 2)
- **PSM 11**: 40-53% hit rate across columns
- **PSM 12**: 40-46% hit rate across columns

## Comparison with TSV Results

The hOCR results show significant improvement over TSV:
- **Page 2**: 28-53% (hOCR) vs 0-7% (TSV)
- **Page 3**: 25-37% (hOCR) vs 0-14% (TSV)
- **Page 4**: 25-78% (hOCR) vs 0-14% (TSV)
- **Page 5**: 28-61% (hOCR) vs 10-30% (TSV)

## Issues Identified

1. **Still not perfect**: Hit rates are improved but not 100%
2. **Inconsistent performance**: Some columns perform much better than others
3. **Over-detection**: hOCR detects more words, including noise

## Recommendations

1. **Use hOCR as primary source**: hOCR provides better content detection
2. **Combine with column detection**: Use hOCR words with improved column detection
3. **Filter low-confidence words**: Remove words with low confidence scores
4. **Post-process results**: Apply text normalization and correction

## Next Steps

1. Implement column detection using hOCR bounding boxes
2. Test with filtered high-confidence words
3. Combine hOCR with improved column detection algorithms
4. Test the complete pipeline with the expected output format

## Files

- `hocr_hit_rate_analysis/hocr_hit_rate_summary.md`: Summary of hOCR hit rate analysis
- `hocr_hit_rate_analysis/hocr_hit_rate_results.json`: Detailed analysis results

## Conclusion

hOCR output provides significantly better content detection than TSV output, with hit rates ranging from 25% to 78% across different pages and columns. This is a major improvement over the previous 0-30% hit rates with TSV output.





