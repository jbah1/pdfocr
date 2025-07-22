
#!/usr/bin/env python3
"""
Test script for column detection using Tesseract TSV output.
This script implements the column detection algorithm and tests it with page-2.png.
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
                'left': left,
                'top': top,
                'width': width,
                'height': height,
                'text': text,
                'conf': conf
            })

    return data

def detect_columns(word_data, num_columns=3):
    """Detect columns by analyzing word positions with section-based approach."""
    # First, separate header, main content, and footer
    tops = [word['top'] for word in word_data]
    min_top = min(tops)
    max_top = max(tops)

    # Define vertical sections (based on analysis)
    header_threshold = min_top + 200  # First ~200 pixels for headers
    footer_threshold = max_top - 150  # Last ~150 pixels for footers

    # Separate content by vertical position
    header_words = [w for w in word_data if w['top'] < header_threshold]
    main_words = [w for w in word_data if header_threshold <= w['top'] <= footer_threshold]
    footer_words = [w for w in word_data if w['top'] > footer_threshold]

    print(f"Debug - Header words: {len(header_words)}")
    print(f"Debug - Main words: {len(main_words)}")
    print(f"Debug - Footer words: {len(footer_words)}")

    # Process main content for columns
    if not main_words:
        # Fallback if no main content detected
        columns = [word_data]
        return columns

    # Analyze x-coordinate distribution in main content
    x_coords = [word['left'] for word in main_words]
    min_x = min(x_coords)
    max_x = max(x_coords)

    # Create histogram of x-coordinates
    x_histogram = defaultdict(int)
    for x in x_coords:
        x_histogram[x] += 1

    # Find significant gaps between columns
    gaps = []
    prev_x = None
    prev_count = 0

    for x in sorted(x_histogram.keys()):
        if prev_x is not None:
            gap_size = x - prev_x
            # Check if this is a significant gap (low density area)
            if gap_size > 15 and prev_count > 1:  # More strict criteria
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

    print(f"Debug - Column boundaries: {boundaries}")
    print(f"Debug - X-coordinate range: {min_x} to {max_x}")

    # Debug: Show word distribution
    boundary_counts = [0] * (num_columns + 1)
    for word in main_words:
        column_idx = 0
        for i, boundary in enumerate(boundaries):
            if word['left'] < boundary:
                break
            column_idx = i + 1
        boundary_counts[column_idx] += 1

    print(f"Debug - Words per column: {boundary_counts}")

    # Assign main words to columns
    columns = [[] for _ in range(num_columns)]
    for word in main_words:
        column_idx = 0
        for i, boundary in enumerate(boundaries):
            if word['left'] < boundary:
                break
            column_idx = i + 1
        columns[column_idx].append(word)

    # Return header, columns, and footer separately
    return {
        'header': header_words,
        'columns': columns,
        'footer': footer_words
    }

def format_markdown(result):
    """Format detected columns as markdown."""
    markdown = []

    # Format header
    if result['header']:
        header_words = sorted(result['header'], key=lambda w: (w['top'], w['left']))
        header_lines = []

        # Group header words by line
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

        footer_words = sorted(result['footer'], key=lambda w: (w['top'], w['left']))
        footer_lines = []

        # Group footer words by line
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

def main():
    """Test column detection with Tesseract TSV output."""
    import sys

    # Get filename from command line arguments
    filename = 'docs/page-2.png'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not filename.startswith('docs/'):
            filename = f'docs/{filename}'

    print(f"Testing column detection with {filename}...")

    # Run Tesseract on the specified file
    tsv_data = run_tesseract_tsv(filename)
    if not tsv_data:
        print("Failed to get Tesseract output")
        return

    # Parse TSV data
    word_data = parse_tsv_output(tsv_data)
    print(f"Found {len(word_data)} words after filtering")

    # Detect columns
    result = detect_columns(word_data, num_columns=3)

    print(f"Detected {len(result['columns'])} columns")
    for i, column in enumerate(result['columns']):
        print(f"Column {i+1}: {len(column)} words")

    print(f"Header words: {len(result['header'])}")
    print(f"Footer words: {len(result['footer'])}")

    # Format as markdown
    markdown = format_markdown(result)
    print("\nGenerated Markdown:")
    print("=" * 50)
    print(markdown)
    print("=" * 50)

if __name__ == '__main__':
    main()
