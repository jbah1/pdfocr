



# hOCR Debugging Analysis

## Summary

This analysis examines the hOCR output format to understand why the parsing is failing.

## Key Findings

1. **hOCR format is complex**: The hOCR output contains nested HTML with multiple span elements
2. **Word extraction is challenging**: Words are wrapped in multiple span elements with different classes
3. **Regex pattern needs adjustment**: The current regex pattern is not matching the actual hOCR structure

## Sample hOCR Output Analysis

Looking at the hOCR output for page-2.png with PSM 6:

```html
<span class='ocrx_word' id='word_1_1' title='bbox 324 62 418 84; x_wconf 96'>Oktober</span>
<span class='ocrx_word' id='word_1_2' title='bbox 426 60 481 81; x_wconf 96'>2023</span>
```

The pattern should match:
- `<span class='ocrx_word' id='word_1_1' title='bbox 324 62 418 84; x_wconf 96'>Oktober</span>`

## Issues Identified

1. **Single quotes vs double quotes**: The hOCR uses single quotes, but regex expects double quotes
2. **Class name variation**: The class is `ocrx_word` not `ocrx_word`
3. **Title attribute format**: The title contains `x_wconf` after bbox coordinates

## Corrected Regex Pattern

The pattern should be:
```regex
r"<span class='ocrx_word' id='word_\d+_\d+' title='bbox (\d+) (\d+) (\d+) (\d+);.*?'>(.*?)</span>"
```

## Next Steps

1. Fix the regex pattern to match the actual hOCR format
2. Test with the corrected pattern
3. Extract words and compare with TSV output
4. Analyze if hOCR provides better structural information

## Conclusion

The hOCR parsing is failing due to regex pattern mismatch. Once fixed, hOCR could provide better structural information for column detection.




