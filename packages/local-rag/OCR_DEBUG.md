# Local RAG OCR Debugging Guide

## Quick Test Command

```bash
cd packages/local-rag
PYTHONUNBUFFERED=1 PYTHONPATH=. OCR_ENGINE=tesseract OCR_MAX_PAGES=3 \
python debug_ocr.py /path/to/your/file.pdf
```

## What the Enhanced Logging Shows

With the updated code, you'll now see:

```
PDF: Reading file.pdf...
PDF: Found 5 pages
PDF: Average 45 chars/page
PDF: OCR required for file.pdf...
PDF: Running OCRmyPDF (lang=eng)...
PDF: OCR complete, extracting text...
PDF: Extracted 1234 chars from OCR
```

If OCRmyPDF fails (missing dependency, corrupted PDF), the code falls back to image-based OCR with Tesseract and logs:
```
PDF OCR failed: ...
PDF: Falling back to image-based OCR...
OCR: Processing image 1/3...
OCR: Image 1 - running Tesseract...
```

## If It Hangs

Tesseract is much more stable than PaddleOCR, but a few places can still stall:

**At "PDF: Reading..."** → Corrupted PDF or too large
- Try with a smaller/different PDF
- Check file size: `ls -lh file.pdf`

**At "PDF: Running OCRmyPDF"** → Usually missing dependencies (tesseract, qpdf, ghostscript)
- On macOS: `brew install tesseract qpdf ghostscript poppler`
- On Ubuntu: `sudo apt install tesseract-ocr qpdf ghostscript poppler-utils`
- If the PDF has native text, set `OCR_ENABLED=false` to skip OCR entirely.

## Handling Slow Pages

Tesseract is generally fast, but if a specific page is slow:
- Lower DPI for that PDF: `OCR_PAGE_DPI=150`
- Run `ocrmypdf` manually on the PDF to confirm it completes
- If it repeatedly hangs, skip OCR (`OCR_ENABLED=false`) after preprocessing

## Common Issues

1. **Missing system deps**: Install `tesseract-ocr`, `qpdf`, `ghostscript`, and `poppler-utils`.
2. **OCR output is empty**: Bump `OCR_PAGE_DPI` to 300 for scanned PDFs.
3. **Language not recognized**: Set `OCR_LANG=eng+heb` (comma or plus separated).
4. **Large images**: Files with >80M pixels are skipped to avoid memory issues.
