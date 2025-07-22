

#!/usr/bin/env python3
"""
Analyze and compare Tesseract PSM mode results.
"""

import os
from pathlib import Path
import re

def analyze_tsv_file(tsv_file):
    """Analyze a TSV file and extract key information."""
    try:
        with open(tsv_file, 'r') as f:
            lines = f.readlines()

        if not lines:
            return {
                'total_lines': 0,
                'level_5_count': 0,
                'sample_words': [],
                'has_column_info': False
            }

        # Check if this is a minimal output (PSM 13)
        if len(lines) <= 5:
            return {
                'total_lines': len(lines),
                'level_5_count': 0,
                'sample_words': [],
                'has_column_info': False,
                'is_minimal': True
            }

        # Parse TSV data
        header = lines[0].strip()
        data_lines = lines[1:]

        level_5_count = 0
        sample_words = []

        for line in data_lines:
            parts = line.strip().split('\t')
            if len(parts) >= 6:  # Level should be in column 6 (index 5)
                try:
                    level = int(parts[5])
                    if level == 5:  # Word level
                        level_5_count += 1
                        if len(sample_words) < 5:
                            word_text = parts[0] if len(parts) > 0 else ""
                            sample_words.append(word_text)
                except ValueError:
                    continue

        return {
            'total_lines': len(lines),
            'level_5_count': level_5_count,
            'sample_words': sample_words,
            'has_column_info': level_5_count > 0,
            'is_minimal': False
        }

    except Exception as e:
        print(f"Error analyzing {tsv_file}: {e}")
        return {
            'total_lines': 0,
            'level_5_count': 0,
            'sample_words': [],
            'has_column_info': False,
            'is_minimal': False
        }

def main():
    # Find all TSV files
    tsv_files = list(Path("psm_comparison").glob("*.tsv"))

    if not tsv_files:
        print("No TSV files found in psm_comparison/")
        return

    print(f"Found {len(tsv_files)} TSV files to analyze\n")

    # Group by page
    page_groups = {}
    for tsv_file in tsv_files:
        match = re.match(r'page-(\d+)-psm(\d+)\.tsv', tsv_file.name)
        if match:
            page_num = match.group(1)
            psm_mode = int(match.group(2))

            if page_num not in page_groups:
                page_groups[page_num] = {}

            page_groups[page_num][psm_mode] = tsv_file

    # Analyze each page group
    for page_num, psm_files in page_groups.items():
        print(f"Page {page_num}:")

        for psm_mode, tsv_file in psm_files.items():
            analysis = analyze_tsv_file(tsv_file)

            print(f"  PSM {psm_mode}:")
            print(f"    Total lines: {analysis['total_lines']}")
            print(f"    Level 5 (word) entries: {analysis['level_5_count']}")

            if not analysis['is_minimal']:
                if analysis['level_5_count'] > 0:
                    print(f"    Sample words: {', '.join(analysis['sample_words'])}")
                else:
                    print(f"    Sample words: (none found)")

            print(f"    {'Has word-level data' if analysis['level_5_count'] > 0 else 'No word-level data'}")

        print()

    print("Analysis complete!")

if __name__ == "__main__":
    main()

