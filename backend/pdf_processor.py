
"""
PDF processing module using Tesseract for OCR and column detection.
Replaces PyMuPDF and Pillow dependencies.
"""

import subprocess
import tempfile
import os
from typing import List, Dict, Optional

def pdf_to_png(pdf_path: str, output_dir: str) -> List[str]:
    """Convert PDF to PNG images using pdftoppm (poppler-utils)."""
    png_files = []
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Use pdftoppm to convert PDF to PNG at 300 DPI
        output_pattern = os.path.join(output_dir, "page")
        cmd = [
            "pdftoppm",
            "-png",
            "-scale-to", "1200",  # Scale to 1200 pixels height for reasonable resolution
            pdf_path,
            output_pattern
        ]


        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"PDF conversion failed: {result.stderr}")


        # Find all generated PNG files
        for i in range(1, 100):  # Support up to 99 pages
            png_file = f"{output_pattern}-{i}.png"
            if os.path.exists(png_file):
                png_files.append(png_file)
            else:
                break

    except Exception as e:
        print(f"Error converting PDF to PNG: {e}")

    return png_files

def run_tesseract_tsv(png_file: str) -> Optional[str]:
    """Run Tesseract on a PNG file and return TSV output."""
    try:
        # Run Tesseract with TSV output
        cmd = [
            "tesseract",
            png_file,
            "stdout",
            "--psm", "3",  # Fully automatic page segmentation
            "--oem", "1",  # LSTM OCR engine
            "-l", "nld",   # Dutch language
            "tsv"
        ]
        print(f"DEBUG: Running Tesseract command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        print(f"DEBUG: Tesseract return code: {result.returncode}")
        print(f"DEBUG: Tesseract stdout length: {len(result.stdout)}")
        print(f"DEBUG: Tesseract stderr: {result.stderr}")

        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Tesseract failed: {e}")
        print(f"Tesseract stderr: {e.stderr}")
        return None

def parse_tsv_output(tsv_data: str) -> List[Dict]:
    """Parse Tesseract TSV output into structured word data."""
    lines = tsv_data.strip().split('\n')
    word_data = []

    for line in lines:
        parts = line.split('\t')
        if len(parts) >= 11:
            # Skip header line (where first part is not a number)
            if not parts[0].isdigit():
                continue
            try:
                level = int(parts[0])
                if level == 5:  # Word level
                    word = {
                        'level': level,
                        'page_num': int(parts[1]),
                        'block_num': int(parts[2]),
                        'par_num': int(parts[3]),
                        'line_num': int(parts[4]),
                        'word_num': int(parts[5]),
                        'left': int(parts[6]),
                        'top': int(parts[7]),
                        'width': int(parts[8]),
                        'height': int(parts[9]),
                        'conf': int(parts[10]),
                        'text': parts[11] if len(parts) > 11 else ''
                    }
                    word_data.append(word)
            except ValueError:
                continue

    return word_data

def detect_columns(word_data: List[Dict], num_columns: int = 3) -> Dict:
    """Detect columns in word data using x-coordinate gaps."""
    # Filter out non-word elements and empty text
    words = [w for w in word_data if w['text'].strip()]

    if not words:
        return {'header': [], 'columns': [[] for _ in range(num_columns)], 'footer': []}

    # Sort words by top position (vertical) then left position (horizontal)
    words.sort(key=lambda w: (w['top'], w['left']))

    # Separate header, main content, and footer based on vertical position
    min_y = min(w['top'] for w in words)
    max_y = max(w['top'] + w['height'] for w in words)
    page_height = max_y - min_y

    # Estimate header and footer thresholds
    header_threshold = min_y + page_height * 0.15
    footer_threshold = max_y - page_height * 0.15

    header_words = [w for w in words if w['top'] < header_threshold]
    footer_words = [w for w in words if w['top'] > footer_threshold]
    main_words = [w for w in words if header_threshold <= w['top'] <= footer_threshold]

    # Find column boundaries by analyzing x-coordinate gaps
    x_coords = [w['left'] for w in main_words]
    min_x = min(x_coords)
    max_x = max(x_coords)

    # Create histogram of x-coordinates
    x_histogram = {}
    for x in x_coords:
        x_histogram[x] = x_histogram.get(x, 0) + 1

    # Find gaps between columns
    gaps = []
    sorted_x = sorted(x_histogram.keys())
    prev_x = None
    prev_count = 0

    for x in sorted_x:
        if prev_x is not None and (x - prev_x) > 20 and prev_count > 5:
            gaps.append((prev_x, x))

        prev_x = x
        prev_count = x_histogram[x]

    # Determine column boundaries
    if not gaps:
        # Fallback: use even distribution
        column_width = (max_x - min_x) // num_columns
        boundaries = [min_x + i * column_width for i in range(1, num_columns)]
    else:
        # Use detected gaps, sorted by position
        # We need num_columns-1 boundaries to create num_columns columns
        all_boundaries = [gap[1] for gap in sorted(gaps)]
        if len(all_boundaries) >= num_columns - 1:
            boundaries = all_boundaries[:num_columns-1]
        else:
            # Not enough gaps, use even distribution as fallback
            column_width = (max_x - min_x) // num_columns
            boundaries = [min_x + i * column_width for i in range(1, num_columns)]

    # Assign main words to columns
    columns = [[] for _ in range(num_columns)]
    for word in main_words:
        column_idx = 0
        for i, boundary in enumerate(boundaries):
            if word['left'] < boundary:
                break
            column_idx = i + 1
        columns[column_idx].append(word)

    return {
        'header': header_words,
        'columns': columns,
        'footer': footer_words
    }

def format_markdown(result: Dict) -> str:
    """Format detected columns as markdown."""
    markdown = []

    # Format header
    if result['header']:
        header_words = result['header']
        header_words.sort(key=lambda w: (w['top'], w['left']))

        # Group header words by line
        header_lines = []
        current_line = []
        current_top = None
        line_tolerance = 10

        for word in header_words:
            if current_top is None or abs(word['top'] - current_top) <= line_tolerance:
                current_line.append(word)
                current_top = word['top']
            else:
                # Process current line
                line_text = ' '.join(word['text'] for word in current_line)
                header_lines.append(line_text)
                current_line = [word]
                current_top = word['top']

        # Add last line
        if current_line:
            line_text = ' '.join(word['text'] for word in current_line)
            header_lines.append(line_text)

        markdown.extend(header_lines)
        markdown.append('')  # Add blank line after header

    # Format columns
    for i, column in enumerate(result['columns']):
        if not column:
            continue

        # Add column header
        markdown.append(f"# Column {i+1}:")
        markdown.append('')

        # Sort words by top position, then left position
        column.sort(key=lambda w: (w['top'], w['left']))

        # Group words by line (vertical proximity)
        current_line = []
        current_top = None
        line_tolerance = 10

        for word in column:
            if current_top is None or abs(word['top'] - current_top) <= line_tolerance:
                current_line.append(word)
                current_top = word['top']
            else:
                # Process current line
                line_text = ' '.join(word['text'] for word in current_line)
                markdown.append(line_text)
                current_line = [word]
                current_top = word['top']

        # Add last line
        if current_line:
            line_text = ' '.join(word['text'] for word in current_line)
            markdown.append(line_text)

        # Add blank line between columns
        markdown.append('')

    # Format footer
    if result['footer']:
        if markdown and markdown[-1] != '':
            markdown.append('')  # Add blank line before footer

        footer_words = result['footer']
        footer_words.sort(key=lambda w: (w['top'], w['left']))

        # Group footer words by line
        footer_lines = []
        current_line = []
        current_top = None
        line_tolerance = 10

        for word in footer_words:
            if current_top is None or abs(word['top'] - current_top) <= line_tolerance:
                current_line.append(word)
                current_top = word['top']
            else:
                # Process current line
                line_text = ' '.join(word['text'] for word in current_line)
                footer_lines.append(line_text)
                current_line = [word]
                current_top = word['top']

        # Add last line
        if current_line:
            line_text = ' '.join(word['text'] for word in current_line)
            footer_lines.append(line_text)

        markdown.extend(footer_lines)

    return '\n'.join(markdown)

def process_pdf_to_markdown(pdf_path: str, temp_dir: str = "/tmp") -> str:
    """Process a PDF file and convert it to markdown with column detection."""
    # Convert PDF to PNG images
    png_files = pdf_to_png(pdf_path, temp_dir)

    if not png_files:
        return "# Error: Failed to convert PDF to images"

    all_markdown = []

    # Process each PNG file
    for i, png_file in enumerate(png_files):
        print(f"DEBUG: Processing PNG file: {png_file}")
        print(f"DEBUG: File exists: {os.path.exists(png_file)}")
        # Run Tesseract OCR
        tsv_data = run_tesseract_tsv(png_file)
        if not tsv_data:
            print(f"DEBUG: No TSV data returned for {png_file}")
            continue

        # Debug: Show first few lines of TSV data

        print(f"DEBUG: First 200 chars of TSV data: {tsv_data[:200]}")
        # Show first 10 lines to see if there are any level 5 entries
        lines = tsv_data.strip().split('\n')
        print(f"DEBUG: First 10 lines of TSV data:")
        for i, line in enumerate(lines[:10]):
            print(f"  {i}: {line}")


        # Parse TSV data
        word_data = parse_tsv_output(tsv_data)
        print(f"DEBUG: Parsed {len(word_data)} words from TSV data")

        # Detect columns
        result = detect_columns(word_data, num_columns=3)

        # Format as markdown
        markdown = format_markdown(result)
        print(f"DEBUG: Generated markdown length: {len(markdown)}")

        # Add page header
        page_markdown = f"# Page {i+1}\n\n{markdown}"
        all_markdown.append(page_markdown)

    # Clean up temporary files
    for png_file in png_files:
        try:
            os.remove(png_file)
        except:
            pass

    return "\n---\n".join(all_markdown)
