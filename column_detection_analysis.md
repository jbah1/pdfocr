

# Column Detection Analysis

## Summary

This analysis compares the column detection results using Tesseract PSM modes 11 and 12 with improved column detection algorithms.

## Key Findings

1. **PSM 11 and 12** produce similar results for column detection
2. The improved algorithm with adaptive gap detection reduces the number of columns significantly
3. Page 2: Reduced from 22 to 19 columns (still too many)
4. Page 5: Reduced from 24 to 10 columns (more reasonable)
5. The algorithm needs further tuning to better handle the specific layout of these pages

## Detailed Results

### Page 2 (PSM 11)
- Words found: 22
- Columns detected: 19
- Sample column content:
  - Column 1: "chef sni"
  - Column 2: "v"
  - Column 3: "olijfolie"
  - Column 4: "bakken pan"
  - Column 5: "leggen"

### Page 5 (PSM 11)
- Words found: 24
- Columns detected: 10
- Sample column content:
  - Column 1: "chocolade"
  - Column 2: "suiker gr Cointreau"
  - Column 3: "oF klein afbakken"
  - Column 4: "met a"
  - Column 5: "losroeren. gieten."

## Issues Identified

1. **Over-segmentation**: Still detecting too many columns (19 for page 2, 10 for page 5)
2. **Single words as columns**: Many columns contain only punctuation or single words
3. **Inconsistent grouping**: Words that should be in the same column are being separated

## Recommendations

1. **Further increase gap threshold**: Try even larger gap values for column detection
2. **Use line-level grouping**: Group words by line first, then detect columns
3. **Post-processing**: Merge small columns (1-2 words) with adjacent columns
4. **Expected column count**: Use domain knowledge (expect 3 columns for recipe pages)

## Next Steps

1. Implement line-level grouping before column detection
2. Add post-processing to merge small columns
3. Test with known column count constraints
4. Evaluate using the expected output format from the conversion plan

## Files

All column detection outputs are available in the `column_outputs/` directory:
- `page-{N}-psm{M}.md` files contain the column detection results
- Files show the current state of column detection with adaptive gap thresholds

