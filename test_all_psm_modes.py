


#!/usr/bin/env python3
"""
Test and compare PSM 6, 11, and 12 for column detection and OCR accuracy.
Generate final column outputs for each page and compare with expected results.
"""

import os
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

def run_tesseract_with_psm(image_path, psm_mode):
    """Run Tesseract with specific PSM mode and return TSV output."""
    try:
        cmd = [
            'tesseract',
            str(image_path),
            'stdout',
            '--psm', str(psm_mode),
            '--oem', '1',
            'tsv'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error: Tesseract failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return None

        return result.stdout

    except Exception as e:
        print(f"Error running tesseract with PSM {psm_mode}: {e}")
        return None

def parse_tsv_output(tsv_data):
    """Parse Tesseract TSV output and extract word information."""
    lines = tsv_data.strip().split('\n')
    if len(lines) < 2:
        return []

    # Skip header
    data_lines = lines[1:]

    words = []
    for line in data_lines:
        parts = line.strip().split('\t')
        if len(parts) >= 12:  # Ensure we have enough columns
            try:
                level = int(parts[5])
                if level == 5:  # Word level
                    word_text = parts[11]  # Text is in the last column
                    left = int(parts[6])
                    top = int(parts[7])
                    right = int(parts[8])
                    bottom = int(parts[9])
                    confidence = float(parts[10])

                    words.append({
                        'text': word_text,
                        'left': left,
                        'top': top,
                        'right': right,
                        'bottom': bottom,
                        'confidence': confidence
                    })
            except (ValueError, IndexError):
                continue

    return words

def group_words_by_line(words, max_line_gap=20):
    """Group words by line based on vertical position."""
    if not words:
        return []

    # Sort words by top position, then left position
    words_sorted = sorted(words, key=lambda w: (w['top'], w['left']))

    lines = []
    current_line = []
    last_bottom = -1

    for word in words_sorted:
        # Check if this word is on a new line
        if current_line and (word['top'] - last_bottom > max_line_gap):
            lines.append(current_line)
            current_line = []

        current_line.append(word)
        last_bottom = word['bottom']

    if current_line:
        lines.append(current_line)

    return lines

def detect_columns_from_lines(lines, page_width, max_column_gap=100):
    """Detect columns based on line positions."""
    if not lines:
        return []

    # Sort lines by left position of first word
    lines_sorted = sorted(lines, key=lambda line: line[0]['left'])

    columns = []
    current_column = []
    last_right = -1

    for line in lines_sorted:
        line_left = line[0]['left']
        line_right = line[-1]['right']

        if current_column and (line_left - last_right > max_column_gap):
            columns.append(current_column)
            current_column = []

        current_column.extend(line)
        last_right = line_right

    if current_column:
        columns.append(current_column)

    # If we have too many columns (more than 5), try with a larger gap
    if len(columns) > 5:
        return detect_columns_with_larger_gap(lines, page_width, max_column_gap * 3)

    return columns

def detect_columns_with_larger_gap(lines, page_width, max_column_gap=300):
    """Detect columns with a larger gap threshold."""
    if not lines:
        return []

    # Sort lines by left position of first word
    lines_sorted = sorted(lines, key=lambda line: line[0]['left'])

    columns = []
    current_column = []
    last_right = -1

    for line in lines_sorted:
        line_left = line[0]['left']
        line_right = line[-1]['right']

        if current_column and (line_left - last_right > max_column_gap):
            columns.append(current_column)
            current_column = []

        current_column.extend(line)
        last_right = line_right

    if current_column:
        columns.append(current_column)

    return columns

def format_column_output(columns):
    """Format column output as markdown."""
    output = []
    for i, column in enumerate(columns, 1):
        # Sort column words by top position, then left position
        column_words = sorted(column, key=lambda w: (w['top'], w['left']))
        column_text = ' '.join(word['text'] for word in column_words)
        output.append(f"## Column {i}\n\n{column_text}\n")

    return '\n'.join(output)

def main():
    # Find all page images
    image_files = list(Path(".").glob("page-*.png"))

    if not image_files:
        print("No page images found (page-*.png)")
        return

    print(f"Found {len(image_files)} page images to analyze")

    # Create output directory
    output_dir = Path("final_column_outputs")
    output_dir.mkdir(exist_ok=True)

    # Test PSM modes 6, 11, and 12
    psm_modes = [6, 11, 12]

    for image_file in image_files:
        print(f"\nProcessing {image_file.name}...")

        # Get page number from filename
        page_num = image_file.stem.split('-')[1]

        for psm in psm_modes:
            print(f"  Testing PSM {psm}...")

            # Run Tesseract
            tsv_data = run_tesseract_with_psm(image_file, psm)

            if tsv_data is None:
                print(f"    PSM {psm}: Failed")
                continue

            # Parse TSV output
            words = parse_tsv_output(tsv_data)

            if not words:
                print(f"    PSM {psm}: No words found")
                continue

            # Group words by line
            lines = group_words_by_line(words)

            # Get image dimensions (approximate for column detection)
            page_width = 2500  # Approximate width in pixels

            # Detect columns from lines
            columns = detect_columns_from_lines(lines, page_width)

            # Generate output
            output_content = f"# Page {page_num} - PSM {psm}\n\n"
            output_content += f"Words found: {len(words)}\n"
            output_content += f"Lines detected: {len(lines)}\n"
            output_content += f"Columns detected: {len(columns)}\n\n"
            output_content += format_column_output(columns)

            # Save output
            output_file = output_dir / f"page-{page_num}-psm{psm}.md"
            with open(output_file, 'w') as f:
                f.write(output_content)

            print(f"    PSM {psm}: Success, {len(words)} words, {len(lines)} lines, {len(columns)} columns")

    print(f"\nAll tests completed. Results saved in {output_dir}/")

if __name__ == "__main__":
    main()


