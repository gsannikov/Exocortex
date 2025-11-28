# PaddleOCR System Hang Issue - CRITICAL

## ⚠️ Problem

PaddleOCR causes **system-level hangs** on certain PDFs that can:
- Freeze the entire system
- Require forced reboot
- Cannot be stopped with Python timeouts

**Affected file:** `document.pdf` (4.8MB scanned PDF)

## 🚨 Immediate Workarounds

### Option 1: Disable OCR Entirely
```bash
# Index without OCR
cd packages/local-rag
OCR_ENABLED=false python3 indexer.py /path/to/docs
```

### Option 2: Use Alternative OCR Engine

#### A. Try Surya OCR (Lighter, Python-only)
```bash
pip install surya-ocr

# Use Surya instead of Paddle
OCR_ENGINE=surya python3 indexer.py /path/to/docs
```

#### B. Use External OCR Service (DeepSeek)
```bash
export DEEPSEEK_OCR_URL="https://api.deepseek.com/v1/chat/completions"
export DEEPSEEK_OCR_MODEL="deepseek-chat"
export OCR_ENGINE=deepseek

python3 indexer.py /path/to/docs
```

### Option 3: Pre-process PDFs Externally

Use `pdftotext` or `ocrmypdf` to create searchable PDFs first:
```bash
# Install OCRmyPDF (uses Tesseract OCR)
brew install ocrmypdf tesseract-lang

# Convert scanned PDF to searchable PDF
ocrmypdf --skip-text document.pdf document_searchable.pdf

# Now index the searchable version (no OCR needed)
python3 indexer.py document_searchable.pdf
```

## 🔍 Diagnosis

The file `document.pdf` has:
- 3 pages
- 0 text extracted by pypdf
- Each page is 1653x2339 pixels at 200 DPI
- Triggers OCR processing

PaddleOCR hangs on the first image and cannot be interrupted, even with:
- Python `signal.alarm()` (doesn't work on macOS)
- `ThreadPoolExecutor.result(timeout=60)` (doesn't interrupt low-level ops)
- Process termination (requires system reboot)

## 💡 Recommended Solution

**For production use:**

1. **Default to OCR_ENABLED=false** for safety
2. **Use Tesseract via ocrmypdf** for pre-processing
3. **Only enable PaddleOCR** when:
   - Testing on small/known PDFs first
   - Running in isolated Docker container
   - Have terminal access to kill processes

**For this specific PDF:**
```bash
# Safest approach - use external OCR
ocrmypdf --skip-text --force-ocr \
  "/Users/gursannikov/MyDrive/Finance/Insurance/document.pdf" \
  "/Users/gursannikov/MyDrive/Finance/Insurance/document_ocr.pdf"

# Then index the OCR'd version
OCR_ENABLED=false python3 indexer.py "/Users/gursannikov/MyDrive/Finance/Insurance/document_ocr.pdf"
```

## 🐛 Root Cause

PaddleOCR uses C++ backends (Paddle Inference) that can:
- Deadlock in BLAS/LAPACK operations
- Consume all system resources
- Block at hardware level (GPU/CPU)
- Ignore Python-level interrupts

This is a known issue with Paddle on macOS, especially with:
- Large images (>2000px)
- Certain PDF encodings
- Apple Silicon Macs

## 📝 Files Modified

- `local_rag/ingestion/ocr.py` - Added ThreadPoolExecutor timeout (partial fix)
- `local_rag/ingestion/extractors.py` - Added progress logging
- `debug_ocr.py` - Step-by-step OCR testing
- `OCR_DEBUG.md` - Troubleshooting guide
- `PADDLE_OCR_HANG_ISSUE.md` - This file

## ✅ Next Steps

1. Change default OCR engine from Paddle to Surya or "none"
2. Add warning in documentation about PaddleOCR risks
3. Consider running OCR in separate Docker container with resource limits
4. Add file size/dimension checks before OCR
5. Test with smaller, simpler PDFs first
