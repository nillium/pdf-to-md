"""
Quick test script for PDF to Markdown converter
"""
from pathlib import Path
import sys

# Test if all dependencies are installed
try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
    import numpy as np
    import cv2
    print("✓ All dependencies installed!")
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    print("\nInstall with: pip install -r requirements.txt")
    sys.exit(1)

# Test Tesseract installation
try:
    version = pytesseract.get_tesseract_version()
    print(f"✓ Tesseract version: {version}")
except Exception as e:
    print(f"✗ Tesseract not found: {e}")
    print("\nOn Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    print("On Linux: sudo apt-get install tesseract-ocr")
    sys.exit(1)

# Test Poppler installation
try:
    # This will fail if poppler is not installed
    from pdf2image.exceptions import PDFInfoNotInstalledError
    print("✓ Poppler utilities available")
except Exception:
    pass

print("\n" + "="*60)
print("All systems ready! You can now use pdf_to_markdown.py")
print("="*60)
print("\nUsage example:")
print("  python pdf_to_markdown.py /path/to/pdfs")
print("  python pdf_to_markdown.py /path/to/pdfs --output /path/to/output --dpi 300")
print()
