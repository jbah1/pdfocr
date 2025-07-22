





#!/usr/bin/env python3
"""
Test Tesseract with hOCR output format to get better structural information.
This script tests hOCR output for better column and layout detection.
"""

import os
import subprocess
import sys
from pathlib import Path
from collections import defaultdict
import xml.etree.ElementTree as ET

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

def parse_hocr_output(hocr_data):
    """Parse hOCR output and extract structured information."""
    try:
        # Parse the hOCR XML
        root = ET.fromstring(hocr_data)

        # Find all word elements
        words = []
        for ocr_line in root.findall(".//*[@class='ocr_line']"):
            line_text = ''
            line_box = None

            for ocr_word in ocr_line.findall(".//*[@class='ocrx_word']"):
                word_text = ''
                word_box = None

                # Get word text
                for span in ocr_word.findall(".//*[@class='ocrx_cinfo']"):
                    if span.text:
                        word_text = span.text.strip()

                # Get word bounding box
                if 'title' in ocr_word.attrib:
                    bbox = ocr_word.attrib['title']
                    if 'bbox' in bbox:
                        bbox_values = bbox.split(';')[0].split()[1:]
                        if len(bbox_values) == 4:
                            left, top, right, bottom = map(int, bbox_values)
                            word_box = (left, top, right, bottom)

                if word_text and word_box:
                    words.append({
                        'text': word_text,
                        'left': word_box[0],
                        'top': word_box[1],
                        'right': word_box[2],
                        'bottom': word_box[3]
                    })

        return words

    except Exception as e:
        print(f"Error parsing hOCR data: {e}")
        return []

def extract_expected_content():
    """Extract expected content from the conversion plan."""
    expected_content = {
        'page-2': {
            'column_1': [
                "Hazenrug filet;",
                "4 hazenrug filet",
                "Peper zout olijfolie",
                "6 grote champignons 2 sjalot. 1/4",
                "bieslook"
            ],
            'column_2': [
                "Garnituur:",
                "1/2 spitskool",
                "1/4 rode kool",
                "Tijm peper zout, azijn",
                "suiker",
                "Bieten peper zout olijfolie"
            ],
            'column_3': [
                "Dressing:",
                "50 gr rode wijn azijn,",
                "2 sjalotjes, 100 gr",
                "zonnebloem olie, peper, zout"
            ]
        },
        'page-3': {
            'column_1': [
                "Patrijs met rode pootjes:",
                "5 x patrijs",
                "Peper, zout",
                "Fond 2 bakjes, 1 bakje water"
            ],
            'column_2': [
                "Garnituur:",
                "Witlof 8/10 stronkjes",
                "Peper, zout, honing",
                "4 aardappels",
                "3 witte uien, 2 dl rode wijn",
                "azijn, 2/4 lepels suiker"
            ],
            'column_3': [
                "Ananas saus:",
                "2 bakjes fond 1/4 ananas",
                "Peper, zout"
            ]
        },
        'page-4': {
            'column_1': [
                "Hertenhaas filet:",
                "2 filets",
                "peper, zout, olijfolie"
            ],
            'column_2': [
                "Groenten:",
                "3 peren/ amandel schaafsel",
                "250 gr paddenstoelen/3 sjalot",
                "5 pp gr spruiten/ spekje",
                "250 gr orzo 1/4 bieslook"
            ],
            'column_3': [
                "Saus :",
                "6 dl fond 2 dl rode wijn",
                "2 sjalotjes 100 gr boter",
                "Wild kruid"
            ]
        },
        'page-5': {
            'column_1': [
                "Appeltje:",
                "10 appeltjes frangipane/of spijs",
                "Suiker",
                "Poedersuiker",
                "Bladerdeeg 3 plakjes"
            ],
            'column_2': [
                "Parfait:",
                "5 eidooiers en 2 eieren",
                "100 gr suiker",
                "400 gr room",
                "6 speculaas"
            ],
            'column_3': [
                "koekje:",
                "3 plakje bladerdeeg",
                "Suiker kaneel, water"
            ]
        }
    }

    return expected_content

def analyze_hit_rate(actual_words, expected_words):
    """Analyze how many expected words are found in actual OCR results."""
    actual_text = ' '.join(word['text'].lower() for word in actual_words)
    expected_text = ' '.join(expected_words).lower()

    expected_set = set(expected_text.split())
    actual_set = set(actual_text.split())

    hits = expected_set.intersection(actual_set)
    total_expected = len(expected_set)

    hit_rate = len(hits) / total_expected if total_expected > 0 else 0

    return {
        'hit_rate': hit_rate,
        'hits': hits,
        'expected': expected_set,
        'actual': actual_set,
        'expected_count': total_expected,
        'hit_count': len(hits)
    }

def main():
    # Find all page images
    image_files = list(Path(".").glob("page-*.png"))

    if not image_files:
        print("No page images found (page-*.png)")
        return

    print(f"Found {len(image_files)} page images to analyze")

    # Get expected content
    expected_content = extract_expected_content()

    # Create output directory
    output_dir = Path("hocr_results")
    output_dir.mkdir(exist_ok=True)

    # Test PSM modes 6, 11, and 12 with hOCR output
    psm_modes = [6, 11, 12]

    all_results = {}

    for image_file in image_files:
        print(f"\nProcessing {image_file.name}...")

        # Get page number from filename
        page_num = image_file.stem.split('-')[1]
        page_key = f"page-{page_num}"

        if page_key not in expected_content:
            print(f"  No expected content for {page_key}, skipping...")
            continue

        page_results = {
            'page': page_key,
            'expected': expected_content[page_key],
            'psm_results': {}
        }

        for psm in psm_modes:
            print(f"  Testing PSM {psm} with hOCR output...")

            # Run Tesseract with hOCR output
            hocr_data = run_tesseract_hocr(image_file, psm, 'nld')

            if hocr_data is None:
                print(f"    PSM {psm}: Failed")
                continue

            # Parse hOCR output
            words = parse_hocr_output(hocr_data)

            if not words:
                print(f"    PSM {psm}: No words found")
                continue

            # Analyze hit rate for each expected column
            psm_result = {
                'words': words,
                'column_analysis': {}
            }

            for col_name, expected_lines in expected_content[page_key].items():
                expected_text = ' '.join(expected_lines)
                expected_words = expected_text.split()

                analysis = analyze_hit_rate(words, expected_words)

                psm_result['column_analysis'][col_name] = {
                    'expected_words': expected_words,
                    'expected_count': analysis['expected_count'],
                    'hit_count': analysis['hit_count'],
                    'hit_rate': analysis['hit_rate'],
                    'hits': list(analysis['hits'])
                }

            page_results['psm_results'][f"psm{psm}"] = psm_result
            print(f"    PSM {psm}: Success, {len(words)} words found")

        all_results[page_key] = page_results

    # Generate summary report
    summary_output = "# hOCR Output Analysis Summary\n\n"

    for page_key, page_data in all_results.items():
        summary_output += f"## Page {page_key}\n\n"

        for psm, psm_data in page_data['psm_results'].items():
            summary_output += f"### PSM {psm}\n"
            summary_output += f"Words found: {len(psm_data['words'])}\n\n"

            for col_name, col_analysis in psm_data['column_analysis'].items():
                summary_output += f"- **{col_name}**: {col_analysis['hit_count']}/{col_analysis['expected_count']} words found ({col_analysis['hit_rate']:.2%})\n"

            summary_output += "\n"

    # Save summary report
    summary_file = output_dir / "hocr_summary.md"
    with open(summary_file, 'w') as f:
        f.write(summary_output)

    # Save detailed results
    detailed_file = output_dir / "hocr_results.json"
    import json
    with open(detailed_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\nAnalysis completed. Results saved in {output_dir}/")
    print(f"Summary: {summary_file}")
    print(f"Detailed results: {detailed_file}")

if __name__ == "__main__":
    main()





