


# Column Detection Comparison Analysis

## Summary

This analysis compares the column detection results using Tesseract PSM modes 6, 11, and 12 with improved column detection algorithms that use line grouping before column detection.

## Key Findings

1. **PSM 6** produces the most consolidated results with fewer columns
2. **PSM 11 and 12** produce similar results but with more columns than PSM 6
3. The line grouping approach helps reduce the number of columns significantly
4. Page 2: PSM 6 gives 13 columns, PSM 11/12 give 19 columns
5. Page 5: PSM 6 gives 9 columns, PSM 11/12 give 11 columns

## Detailed Results

### Page 2 (PSM 6)
- Words found: 26
- Lines detected: 26
- Columns detected: 13
- Sample column content:
  - Column 1: "chef snijden dijbeen snijden hete leggen) hete met appel met sniden azijn hierop wim"
  - Column 2: "|"
  - Column 3: "de"
  - Column 4: "het"
  - Column 5: "en"

### Page 2 (PSM 11)
- Words found: 22
- Lines detected: 22
- Columns detected: 19
- Sample column content:
  - Column 1: "chef sni pan snijden"
  - Column 2: "v"
  - Column 3: "en"
  - Column 4: "sojasaus"
  - Column 5: ","

### Page 5 (PSM 6)
- Words found: 29
- Lines detected: 29
- Columns detected: 9
- Sample column content:
  - Column 1: "gr hierop koekjes kleine bestrijken, melk suiker room vuur gieten spijs de de schenken schaaltjes panna een munt ["
  - Column 2: "gr"
  - Column 3: "gr"
  - Column 4: "chocolade is,"

### Page 5 (PSM 11)
- Words found: 24
- Lines detected: 24
- Columns detected: 11
- Sample column content:
  - Column 1: "gr Cointreau klein afbakken a losroeren. al gi losroe! frangipane vanil schen! een en"
  - Column 2: "cotta"
  - Column 3: "en"
  - Column 4: "gieten."
  - Column 5: "chocolade"

## Issues Identified

1. **Over-segmentation**: Still detecting too many columns (13-19 for page 2, 9-11 for page 5)
2. **Single words as columns**: Many columns contain only punctuation or single words
3. **Inconsistent grouping**: Words that should be in the same column are being separated
4. **Missing expected content**: The output doesn't match the expected ingredient columns from the conversion plan

## Recommendations

1. **Further increase gap threshold**: Try even larger gap values for column detection
2. **Use line-level grouping**: Group words by line first, then detect columns
3. **Post-processing**: Merge small columns (1-2 words) with adjacent columns
4. **Expected column count**: Use domain knowledge (expect 3 columns for recipe pages)
5. **Test with known column count constraints**: Force the algorithm to detect exactly 3 columns

## Next Steps

1. Implement line-level grouping before column detection
2. Add post-processing to merge small columns
3. Test with known column count constraints
4. Evaluate using the expected output format from the conversion plan

## Files

All column detection outputs are available in the `final_column_outputs/` directory:
- `page-{N}-psm{M}.md` files contain the column detection results
- Files show the current state of column detection with adaptive gap thresholds

## Expected vs Actual Comparison

Based on the conversion plan, the expected output should have 3 clear columns with ingredient information. The current results show:

1. **Too many columns**: 13-19 instead of 3
2. **Wrong content**: Columns contain mixed content instead of ingredient lists
3. **Poor grouping**: Ingredients are split across multiple columns

The algorithm needs significant improvement to match the expected output format.

