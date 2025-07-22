

"""
Test script for the backend PDF processing.
"""

import os
from pdf_processor import process_pdf_to_markdown

def test_pdf_processing():
    """Test the PDF processing with the sample PDF."""
    # Use the sample PDF from the docs directory
    pdf_path = "../docs/2023-10 kwartel, kabeljauw, kalf, bananenrol.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    print("Processing PDF...")
    markdown = process_pdf_to_markdown(pdf_path)

    # Print the first 1000 characters of the result
    print("Markdown output (first 1000 chars):")
    print(markdown[:1000])
    print("\n...")

    # Save full output to a file
    output_file = "test_output.md"
    with open(output_file, 'w') as f:
        f.write(markdown)

    print(f"Full output saved to {output_file}")
    print(f"Total length: {len(markdown)} characters")

if __name__ == "__main__":
    test_pdf_processing()

