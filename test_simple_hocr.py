





#!/usr/bin/env python3
"""
Simple test to examine hOCR output format and extract basic information.
"""

import os
import subprocess
import sys
from pathlib import Path
import re

def run_tesseract_hocr(image_path, psm_mode, lang='nld'):
    """Run Tesseract with hOCR output format."""
    try:
        cmd = [
            'tesseract',
            str(image_path),
            'stdout',
            '--psm', str(psm_mode),
            '--oem', '1',
            '-l', lang,
            'hocr'
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

def extract_words_from_hocr(hocr_data):
    """Extract words from hOCR data using regex."""
    words = []

    # Extract all ocrx_word elements with their bbox and text
    # Note: hOCR uses single quotes, and the pattern needs to handle the actual format
    pattern = r"<span class='ocrx_word' id='word_\d+_\d+' title='bbox (\d+) (\d+) (\d+) (\d+);.*?'>(.*?)</span>"
    matches = re.finditer(pattern, hocr_data, re.DOTALL)

    for match in matches:
        left = int(match.group(1))
        top = int(match.group(2))
        right = int(match.group(3))
        bottom = int(match.group(4))
        text = match.group(5).strip()

        # Remove any HTML tags from the text
        text = re.sub(r'<[^>]+>', '', text)

        if text:
            words.append({
                'text': text,
                'left': left,
                'top': top,
                'right': right,
                'bottom': bottom
            })

    return words

def main():
    # Find all page images
    image_files = list(Path(".").glob("page-*.png"))

    if not image_files:
        print("No page images found (page-*.png)")
        return

    print(f"Found {len(image_files)} page images to analyze")

    # Test PSM modes 6, 11, and 12 with hOCR output
    psm_modes = [6, 11, 12]

    # Create output directory
    output_dir = Path("simple_hocr_results")
    output_dir.mkdir(exist_ok=True)

    for image_file in image_files:
        print(f"\nProcessing {image_file.name}...")

        for psm in psm_modes:
            print(f"  Testing PSM {psm} with hOCR output...")

            # Run Tesseract with hOCR output
            hocr_data = run_tesseract_hocr(image_file, psm, 'nld')

            if hocr_data is None:
                print(f"    PSM {psm}: Failed")
                continue

            # Save raw hOCR output for analysis
            hocr_file = output_dir / f"{image_file.stem}-psm{psm}.hocr"
            with open(hocr_file, 'w') as f:
                f.write(hocr_data)

            # Extract words using regex
            words = extract_words_from_hocr(hocr_data)

            print(f"    PSM {psm}: Found {len(words)} words")

            # Save extracted words
            words_file = output_dir / f"{image_file.stem}-psm{psm}.json"
            import json
            with open(words_file, 'w') as f:
                json.dump(words, f, indent=2)

            # Show sample words
            if words:
                print(f"    Sample words: {words[:3]}")

    print(f"\nAnalysis completed. Results saved in {output_dir}/")

if __name__ == "__main__":
    main()





