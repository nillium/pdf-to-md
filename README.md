# PDF to Markdown Converter

> Convert PDF files to Markdown with OCR text extraction, automatic figure/equation detection, and LaTeX conversion.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **📝 OCR Text Extraction** - Extracts all text from PDFs using Tesseract OCR at 200 DPI (configurable)
- **📊 Figure Detection** - Automatically detects and extracts figures and diagrams
- **🔢 Equation Extraction** - Identifies equations and converts them to LaTeX format
- **📸 Side-by-side Display** - Shows LaTeX rendering and original screenshot for equations
- **📝 Clean Markdown Output** - Generates well-formatted Markdown with embedded images
- **⚡ Batch Processing** - Process entire folders of PDFs at once

## 🚀 Quick Start

### Installation

**1. Install System Dependencies:**

**Windows:**
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) - Add to PATH
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) - Extract and add to PATH

**Linux:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

**2. Install Python Packages:**

```bash
pip install -r requirements.txt
```

**3. Test Installation:**

```bash
python test_dependencies.py
```

### Usage

**Basic conversion:**
```bash
python pdf_to_markdown.py /path/to/pdfs
```

**High quality (300 DPI):**
```bash
python pdf_to_markdown.py /path/to/pdfs --dpi 300
```

**Custom output directory:**
```bash
python pdf_to_markdown.py /path/to/pdfs --output /path/to/output
```

## 📚 Example

**Input:** `Heat_Transfer.pdf` (Engineering textbook)

**Output:**
```
Heat_Transfer.md                    # Markdown file with all content
Heat_Transfer_images/               # Extracted images folder
├── page001_equation_1.png
├── page001_figure_2.png
├── page002_equation_3.png
└── ...
```

**Markdown Preview:**

```markdown
## Page 1

The fundamental law of heat conduction states that...

<div style="display: flex; align-items: center; gap: 20px;">
  <div style="flex: 1;">
  
  **Equation (LaTeX):**
  
  $$
  q = -kA\frac{dT}{dx}
  $$
  
  </div>
  <div style="flex: 1;">
  
  **Original:**
  
  ![Equation](Heat_Transfer_images/page001_equation_1.png)
  
  </div>
</div>
```

## 🛠️ Configuration

Edit these parameters in `pdf_to_markdown.py`:

```python
DPI = 200                  # Image quality (100-600)
MIN_EQUATION_HEIGHT = 20   # Equation detection threshold
MIN_FIGURE_SIZE = 100      # Figure minimum size (pixels)
```

## 📊 Performance

| Metric | Value |
|--------|-------|
| Processing Speed | ~1-2 min/page @ 200 DPI |
| Memory Usage | ~500MB per page |
| Storage | ~2-5MB per page |

## 📄 Documentation

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Fast installation guide
- **[DOCUMENTATION.md](docs/DOCUMENTATION.md)** - Complete user guide
- **[FEATURES.md](docs/FEATURES.md)** - Detailed feature list

## 🔍 Improving LaTeX Accuracy

The built-in converter uses heuristics. For better results:

**Option 1: pix2tex (Free, AI-based)**
```bash
pip install pix2tex
```

**Option 2: MathPix API (Commercial)**
- Very accurate equation recognition
- Requires API key
- https://mathpix.com/

## 📱 Best Markdown Viewers

For viewing output with LaTeX equations:
- **Obsidian** ⭐ - Excellent for equations and linking
- **Typora** - Beautiful rendering
- **VS Code** - With Markdown Preview Enhanced extension
- **Notion** - Import .md files directly

## 🐛 Troubleshooting

**"Tesseract not found"**
```bash
# Windows - Add to PATH
$env:PATH += ";C:\Program Files\Tesseract-OCR"

# Linux
sudo apt-get install tesseract-ocr
```

**"poppler not found"**
- **Windows**: Download and add to PATH
- **Linux**: `sudo apt-get install poppler-utils`

## 📜 License

MIT License - feel free to use and modify for your projects.

## 🚀 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## ⭐ Star History

If you find this useful, please consider giving it a star!
