@echo off
REM PDF to Markdown Converter - Quick Run Script
REM Drop this file in your PDF folder and double-click to convert all PDFs

echo ============================================================
echo PDF to Markdown Converter
echo ============================================================
echo.

REM Get the directory where this batch file is located
set "PDF_DIR=%~dp0"

echo Source folder: %PDF_DIR%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if the converter script exists
if not exist "%~dp0pdf_to_markdown.py" (
    echo ERROR: pdf_to_markdown.py not found
    echo Please ensure the script is in the same folder as this batch file
    pause
    exit /b 1
)

echo Running conversion...
echo.

REM Run the converter
python "%~dp0pdf_to_markdown.py" "%PDF_DIR%"

echo.
echo ============================================================
echo Conversion complete!
echo Check the folder for .md files and _images folders
echo ============================================================
echo.

pause
