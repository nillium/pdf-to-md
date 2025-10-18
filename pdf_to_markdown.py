#!/usr/bin/env python3
"""
PDF to Markdown Converter with OCR, Image Extraction, and LaTeX Conversion
Processes PDFs to create rich Markdown documents with embedded images and equations
"""

import os
import sys
import re
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageDraw
import numpy as np
import cv2
from typing import List, Tuple, Dict
import argparse

# Configuration
DPI = 200
MIN_EQUATION_HEIGHT = 20  # Minimum height in pixels for equation detection
MIN_FIGURE_SIZE = 100  # Minimum size for figure detection

class PDFToMarkdownConverter:
    def __init__(self, pdf_path: Path, output_dir: Path, dpi: int = DPI):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.dpi = dpi
        self.images_dir = output_dir / f"{pdf_path.stem}_images"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
    def convert(self):
        """Main conversion process"""
        print(f"\n{'='*60}")
        print(f"Converting: {self.pdf_path.name}")
        print(f"{'='*60}\n")
        
        # Convert PDF to images
        print("Step 1: Converting PDF pages to images...")
        pages = convert_from_path(str(self.pdf_path), dpi=self.dpi)
        print(f"✓ Converted {len(pages)} pages\n")
        
        # Process each page
        markdown_content = []
        markdown_content.append(f"# {self.pdf_path.stem}\n\n")
        markdown_content.append(f"*Converted from PDF using OCR at {self.dpi} DPI*\n\n")
        markdown_content.append("---\n\n")
        
        for page_num, page_image in enumerate(pages, 1):
            print(f"Processing page {page_num}/{len(pages)}...")
            page_md = self.process_page(page_image, page_num)
            markdown_content.append(page_md)
            markdown_content.append("\n\n---\n\n")
        
        # Write markdown file
        md_path = self.output_dir / f"{self.pdf_path.stem}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(''.join(markdown_content))
        
        print(f"\n{'='*60}")
        print(f"✓ Conversion complete!")
        print(f"  Output: {md_path}")
        print(f"  Images: {self.images_dir}")
        print(f"{'='*60}\n")
        
        return md_path
    
    def process_page(self, page_image: Image.Image, page_num: int) -> str:
        """Process a single page: extract text, figures, and equations"""
        markdown = []
        markdown.append(f"## Page {page_num}\n\n")
        
        # Convert to numpy array for OpenCV processing
        img_array = np.array(page_image)
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Detect regions of interest (figures, equations)
        print(f"  - Detecting figures and equations...")
        regions = self.detect_regions(img_gray, page_image)
        
        # Get full text with layout info
        print(f"  - Performing OCR...")
        ocr_data = pytesseract.image_to_data(page_image, output_type=pytesseract.Output.DICT)
        
        # Build content with embedded images
        current_y = 0
        text_buffer = []
        
        for region in sorted(regions, key=lambda r: r['y']):
            # Add text before this region
            region_text = self.extract_text_before_y(ocr_data, current_y, region['y'])
            if region_text.strip():
                text_buffer.append(region_text)
            
            # Flush text buffer
            if text_buffer:
                markdown.append(self.clean_text('\n'.join(text_buffer)))
                markdown.append("\n\n")
                text_buffer = []
            
            # Add the region (figure or equation)
            if region['type'] == 'equation':
                markdown.append(self.format_equation_section(region, page_num))
            elif region['type'] == 'figure':
                markdown.append(self.format_figure_section(region, page_num))
            
            current_y = region['y'] + region['height']
        
        # Add remaining text
        remaining_text = self.extract_text_after_y(ocr_data, current_y)
        if remaining_text.strip():
            markdown.append(self.clean_text(remaining_text))
        
        return ''.join(markdown)
    
    def detect_regions(self, img_gray: np.ndarray, page_image: Image.Image) -> List[Dict]:
        """Detect figures and equations in the image"""
        regions = []
        
        # Threshold and detect contours
        _, thresh = cv2.threshold(img_gray, 240, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            
            # Skip small regions
            if w < 50 or h < 20:
                continue
            
            # Determine if it's an equation or figure
            aspect_ratio = w / h
            region_type = 'equation' if (h < 150 and aspect_ratio > 2) else 'figure'
            
            # Skip if too small for figures
            if region_type == 'figure' and (w < MIN_FIGURE_SIZE or h < MIN_FIGURE_SIZE):
                continue
            
            # Extract region
            region_img = page_image.crop((x, y, x + w, y + h))
            
            # Save region image
            img_filename = f"page{len(regions)+1:03d}_{region_type}_{i}.png"
            img_path = self.images_dir / img_filename
            region_img.save(img_path)
            
            # Try to extract LaTeX if it's an equation
            latex = None
            if region_type == 'equation':
                latex = self.image_to_latex(region_img)
            
            regions.append({
                'type': region_type,
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'image_path': img_filename,
                'latex': latex
            })
        
        return regions
    
    def image_to_latex(self, equation_img: Image.Image) -> str:
        """
        Convert equation image to LaTeX
        This is a simplified version - for production, consider using:
        - pix2tex (LaTeX OCR model)
        - MathPix API
        - img2latex models
        """
        # For now, use OCR to extract text and attempt basic conversion
        text = pytesseract.image_to_string(equation_img, config='--psm 6')
        
        # Basic heuristic conversions
        latex = self.text_to_latex_heuristic(text)
        
        return latex
    
    def text_to_latex_heuristic(self, text: str) -> str:
        """
        Basic text to LaTeX conversion using heuristics
        This is simplified - real equation parsing requires specialized models
        """
        text = text.strip()
        
        # Replace common patterns
        replacements = {
            'alpha': r'\alpha',
            'beta': r'\beta',
            'gamma': r'\gamma',
            'delta': r'\delta',
            'theta': r'\theta',
            'lambda': r'\lambda',
            'pi': r'\pi',
            'sigma': r'\sigma',
            '<=': r'\leq',
            '>=': r'\geq',
            '!=': r'\neq',
            '∫': r'\int',
            '∑': r'\sum',
            '∏': r'\prod',
            '√': r'\sqrt',
            '∞': r'\infty',
            '±': r'\pm',
            '×': r'\times',
            '÷': r'\div',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Detect fractions (simple a/b pattern)
        text = re.sub(r'(\w+)/(\w+)', r'\\frac{\1}{\2}', text)
        
        # Detect superscripts (x^2 pattern)
        text = re.sub(r'(\w+)\^(\w+)', r'\1^{\2}', text)
        
        # Detect subscripts (x_i pattern)
        text = re.sub(r'(\w+)_(\w+)', r'\1_{\2}', text)
        
        return text
    
    def format_equation_section(self, region: Dict, page_num: int) -> str:
        """Format equation with LaTeX and screenshot side by side"""
        md = []
        md.append('<div style="display: flex; align-items: center; gap: 20px; margin: 20px 0;">\n')
        md.append('  <div style="flex: 1;">\n\n')
        
        # LaTeX rendering
        if region['latex'] and region['latex'].strip():
            md.append(f"**Equation (LaTeX):**\n\n")
            md.append(f"$$\n{region['latex']}\n$$\n\n")
        else:
            md.append("**Equation:**\n\n")
            md.append("*(LaTeX conversion unavailable)*\n\n")
        
        md.append('  </div>\n')
        md.append('  <div style="flex: 1;">\n\n')
        
        # Screenshot
        md.append(f"**Original:**\n\n")
        md.append(f"![Equation Screenshot]({self.images_dir.name}/{region['image_path']})\n\n")
        
        md.append('  </div>\n')
        md.append('</div>\n\n')
        
        return ''.join(md)
    
    def format_figure_section(self, region: Dict, page_num: int) -> str:
        """Format figure section"""
        md = []
        md.append(f"**Figure:**\n\n")
        md.append(f"![Figure]({self.images_dir.name}/{region['image_path']})\n\n")
        return ''.join(md)
    
    def extract_text_before_y(self, ocr_data: Dict, start_y: int, end_y: int) -> str:
        """Extract text between two y-coordinates"""
        text_parts = []
        n_boxes = len(ocr_data['text'])
        
        for i in range(n_boxes):
            if ocr_data['text'][i].strip():
                y_pos = ocr_data['top'][i]
                if start_y <= y_pos < end_y:
                    text_parts.append(ocr_data['text'][i])
        
        return ' '.join(text_parts)
    
    def extract_text_after_y(self, ocr_data: Dict, start_y: int) -> str:
        """Extract all text after a y-coordinate"""
        text_parts = []
        n_boxes = len(ocr_data['text'])
        
        for i in range(n_boxes):
            if ocr_data['text'][i].strip():
                y_pos = ocr_data['top'][i]
                if y_pos >= start_y:
                    text_parts.append(ocr_data['text'][i])
        
        return ' '.join(text_parts)
    
    def clean_text(self, text: str) -> str:
        """Clean and format text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Add proper paragraph breaks
        sentences = text.split('. ')
        paragraphs = []
        current = []
        
        for sentence in sentences:
            current.append(sentence)
            if len(current) >= 3:  # New paragraph every 3 sentences
                paragraphs.append('. '.join(current) + '.')
                current = []
        
        if current:
            paragraphs.append('. '.join(current))
        
        return '\n\n'.join(paragraphs)


def main():
    parser = argparse.ArgumentParser(
        description='Convert PDF to Markdown with OCR, image extraction, and LaTeX equations'
    )
    parser.add_argument('pdf_folder', type=str, help='Folder containing PDF files')
    parser.add_argument('--output', '-o', type=str, help='Output directory (default: same as input)')
    parser.add_argument('--dpi', type=int, default=200, help='DPI for image extraction (default: 200)')
    
    args = parser.parse_args()
    
    # Setup paths
    pdf_folder = Path(args.pdf_folder)
    if not pdf_folder.exists():
        print(f"Error: Folder '{pdf_folder}' does not exist")
        sys.exit(1)
    
    output_dir = Path(args.output) if args.output else pdf_folder
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all PDFs
    pdf_files = list(pdf_folder.glob('*.pdf'))
    if not pdf_files:
        print(f"No PDF files found in '{pdf_folder}'")
        sys.exit(1)
    
    print(f"\nFound {len(pdf_files)} PDF file(s)")
    print(f"Output directory: {output_dir}")
    print(f"DPI: {args.dpi}\n")
    
    # Process each PDF
    for pdf_path in pdf_files:
        try:
            converter = PDFToMarkdownConverter(pdf_path, output_dir, args.dpi)
            converter.convert()
        except Exception as e:
            print(f"\n✗ Error processing {pdf_path.name}: {str(e)}\n")
            import traceback
            traceback.print_exc()
    
    print("\n✓ All conversions complete!\n")


if __name__ == "__main__":
    main()
