
#!/usr/bin/env python3
"""
Test script to compare Tesseract PSM modes 6, 11, 12, and 13
for column detection and OCR accuracy.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_tesseract_with_psm(image_path, psm_mode, output_file):
    """Run Tesseract with specific PSM mode and save output to file."""
    try:
        # Run tesseract with the specified PSM mode and get TSV output
        cmd = [
            'tesseract',
            str(image_path),
            'stdout',
            '--psm', str(psm_mode),
            '--oem', '1',
            'tsv'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Save the raw TSV output
        with open(output_file, 'w') as f:
            f.write(result.stdout)

        return len(result.stdout), result.returncode

    except Exception as e:
        print(f"Error running tesseract with PSM {psm_mode}: {e}")
        return 0, 1

def main():
    # Create output directory
    output_dir = Path("psm_comparison")
    output_dir.mkdir(exist_ok=True)

    # Find all page images
    image_files = list(Path(".").glob("page-*.png"))

    if not image_files:
        print("No page images found (page-*.png)")
        return

    print(f"Found {len(image_files)} page images to analyze")

    # Test PSM modes 6, 11, 12, 13
    psm_modes = [6, 11, 12, 13]

    for image_file in image_files:
        print(f"\nProcessing {image_file.name}...")

        # Get page number from filename
        page_num = image_file.stem.split('-')[1]

        for psm in psm_modes:
            output_file = output_dir / f"page-{page_num}-psm{psm}.tsv"
            print(f"  Testing PSM {psm}...")

            length, returncode = run_tesseract_with_psm(image_file, psm, output_file)

            if returncode == 0:
                print(f"    PSM {psm}: Success, output length {length}")
            else:
                print(f"    PSM {psm}: Failed with return code {returncode}")

    print(f"\nAll tests completed. Results saved in {output_dir}/")

if __name__ == "__main__":
    main()
