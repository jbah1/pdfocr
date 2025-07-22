

#!/usr/bin/env python3
"""
Analyze the structure of Tesseract TSV output to understand the layout better.
"""

import subprocess
import re
from collections import defaultdict

def run_tesseract_tsv(image_path):
    """Run Tesseract on an image and return TSV output."""
    try:
        result = subprocess.run([
            'tesseract', image_path, 'stdout', '-l', 'nld', '--psm', '1', 'tsv'
        ], capture_output=True, text=True, check=True)

        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running Tesseract: {e}")
        return None

def parse_tsv_output(tsv_data):
    """Parse Tesseract TSV output and return structured data."""
    lines = tsv_data.strip().split('\n')
    data = []

    for line in lines:
        if line.startswith('level'):
            continue  # Skip header

        parts = line.split('\t')
        if len(parts) < 12:
            continue

        level = int(parts[0])
        page_num = int(parts[1])
        block_num = int(parts[2])
        par_num = int(parts[3])
        line_num = int(parts[4])
        word_num = int(parts[5])
        left = int(parts[6])
        top = int(parts[7])
        width = int(parts[8])
        height = int(parts[9])
        conf = float(parts[10]) if parts[10] else 0.0
        text = parts[11] if len(parts) > 11 else ''

        if level == 5 and text and conf != 95.0:  # Word level, exclude noise
            data.append({
                'level': level,
                'block_num': block_num,
                'par_num': par_num,
                'line_num': line_num,
                'word_num': word_num,
                'left': left,
                'top': top,
                'width': width,
                'height': height,
                'text': text,
                'conf': conf
            })

    return data

def analyze_structure(word_data):
    """Analyze the structure of the TSV data."""
    print(f"Total words: {len(word_data)}")

    # Analyze vertical distribution
    tops = [word['top'] for word in word_data]
    min_top = min(tops)
    max_top = max(tops)
    print(f"Vertical range: {min_top} to {max_top}")

    # Group by vertical sections
    section_height = 50
    sections = defaultdict(list)

    for word in word_data:
        section_idx = (word['top'] - min_top) // section_height
        sections[section_idx].append(word)

    print(f"Found {len(sections)} vertical sections")

    # Analyze each section
    for section_idx in sorted(sections.keys()):
        section_words = sections[section_idx]
        lefts = [word['left'] for word in section_words]
        min_left = min(lefts)
        max_left = max(lefts)

        print(f"\nSection {section_idx} (Y: {min_top + section_idx * section_height} to {min_top + (section_idx + 1) * section_height}):")
        print(f"  Words: {len(section_words)}")
        print(f"  Horizontal range: {min_left} to {max_left}")

        # Show sample text
        sample_text = ' '.join(word['text'] for word in section_words[:5])
        print(f"  Sample: {sample_text}")

        # Analyze x-coordinate distribution
        x_histogram = defaultdict(int)
        for left in lefts:
            x_histogram[left] += 1

        # Find significant x-coordinates
        significant_x = sorted([x for x, count in x_histogram.items() if count > 1])
        print(f"  Significant X-coords: {significant_x[:5]}")

def main():
    """Analyze TSV structure for page-2.png."""
    print("Analyzing TSV structure for page-2.png...")

    # Run Tesseract on page-2.png
    tsv_data = run_tesseract_tsv('docs/page-2.png')
    if not tsv_data:
        print("Failed to get Tesseract output")
        return

    # Parse TSV data
    word_data = parse_tsv_output(tsv_data)

    # Analyze structure
    analyze_structure(word_data)

if __name__ == '__main__':
    main()

