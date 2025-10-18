# Quick Start Guide - PDF to Markdown Converter

## Installation (5 minutes)

### Step 1: Install System Dependencies

**Windows:**
1. **Tesseract OCR**: Download installer from https://github.com/UB-Mannheim/tesseract/wiki
   - Run installer, use default location
   - Add to PATH: `C:\Program Files\Tesseract-OCR`

2. **Poppler**: Download from https://github.com/oschwartz10612/poppler-windows/releases
   - Extract to `C:\Program Files\poppler`
   - Add `C:\Program Files\poppler\Library\bin` to PATH

**Linux:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

### Step 2: Install Python Packages

```bash
pip install -r requirements.txt
```

### Step 3: Test Installation

```bash
python test_dependencies.py
```

You should see:
```
✓ All dependencies installed!
✓ Tesseract version: X.X.X
✓ Poppler utilities available
```

## Usage

### Convert a PDF

```bash
python pdf_to_markdown.py "C:\Users\YourName\Documents\PDFs"
```

This will:
1. Find all PDF files in the folder
2. Convert each to Markdown with OCR
3. Extract figures and equations at 200 DPI
4. Create `filename.md` and `filename_images/` folder
5. Convert equations to LaTeX with side-by-side screenshots

### Example Output Structure

```
Documents/PDFs/
├── Heat_Transfer.pdf          (original)
├── Heat_Transfer.md           (generated)
└── Heat_Transfer_images/      (generated)
    ├── page001_equation_1.png
    ├── page001_figure_2.png
    ├── page002_equation_3.png
    └── ...
```

## Advanced Options

### Higher Quality (300 DPI)

```bash
python pdf_to_markdown.py "C:\PDFs" --dpi 300
```

### Custom Output Location

```bash
python pdf_to_markdown.py "C:\PDFs" --output "D:\Markdown"
```

### Batch Processing

Process multiple folders:

```powershell
$folders = @("C:\Books\Math", "C:\Books\Physics", "C:\Books\Engineering")
foreach ($folder in $folders) {
    python pdf_to_markdown.py $folder
}
```

## Viewing the Output

**Best Markdown Viewers:**
- **Obsidian** - Great for equations and images
- **Typora** - Beautiful rendering with LaTeX support
- **VS Code** with Markdown Preview Enhanced
- **Notion** - Import the .md file

## Tips for Best Results

### 1. High-Quality Input
- Use high-resolution scanned PDFs (300+ DPI)
- Ensure good contrast in original documents
- Avoid heavily degraded or photocopied sources

### 2. Equation Recognition
- The built-in converter uses heuristics (basic)
- For better results, install **pix2tex**:
  ```bash
  pip install pix2tex
  ```

### 3. Processing Time
- Expect ~1-2 minutes per page at 200 DPI
- Higher DPI = better quality but slower
- Large PDFs: process in batches

## Troubleshooting

### "No module named 'cv2'"
```bash
pip install opencv-python
```

### "Tesseract is not installed"
**Windows**: Add to PATH in System Environment Variables
```powershell
$env:PATH += ";C:\Program Files\Tesseract-OCR"
```

### "Unable to get page count"
Missing Poppler - install and add to PATH

### Images not showing in viewer
- Check relative paths are correct
- Some viewers need absolute paths
- Ensure image folder is in same directory

## Next Steps

1. **Test with a sample PDF**: Start with a small 1-2 page PDF
2. **Review output**: Check accuracy of OCR and equation conversion
3. **Adjust parameters**: Tweak DPI, region detection thresholds
4. **Customize**: Modify script for your specific needs
