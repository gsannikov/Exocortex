#!/usr/bin/env python3
"""
Debug script to test OCR on a specific PDF file (Python 3.9+ compatible).
Run from packages/local-rag directory with:

PYTHONUNBUFFERED=1 PYTHONPATH=. OCR_ENGINE=tesseract OCR_MAX_PAGES=3 python3 debug_ocr_compat.py <path-to-pdf>
"""
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python3 debug_ocr_compat.py <path-to-pdf>")
    sys.exit(1)

path = Path(sys.argv[1])
if not path.exists():
    print(f"Error: File not found: {path}")
    sys.exit(1)

print(f"Reading {path}", flush=True)
print(f"File size: {path.stat().st_size / (1024*1024):.2f} MB", flush=True)

# Step-by-step debugging
print("\n1. Testing PDF text extraction...", flush=True)
try:
    from pypdf import PdfReader
    r = PdfReader(str(path), strict=False)
    print(f"   Pages: {len(r.pages)}", flush=True)
    texts = [(pg.extract_text() or "") for pg in r.pages]
    avg_text_len = sum(len(t) for t in texts) / max(1, len(texts))
    print(f"   Avg text per page: {avg_text_len:.0f} chars", flush=True)
    print(f"   Will OCR: {avg_text_len < 100}", flush=True)
except Exception as e:
    print(f"   ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n2. Testing pdf2image conversion...", flush=True)
try:
    from pdf2image import convert_from_path
    print("   Converting first page (this may take time)...", flush=True)
    imgs = convert_from_path(str(path), dpi=200, first_page=1, last_page=1)
    print(f"   Converted: {len(imgs)} images", flush=True)
    if imgs:
        print(f"   Image size: {imgs[0].size}", flush=True)
except Exception as e:
    print(f"   ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Testing OCR directly...", flush=True)
try:
    # Import with compatibility for Python 3.9
    import os
    os.environ.setdefault("OCR_ENGINE", "tesseract")
    os.environ.setdefault("OCR_MAX_PAGES", "3")
    
    from local_rag.ingestion.ocr import run_ocr
    from local_rag.settings import get_settings
    
    settings = get_settings()
    print(f"   OCR settings: engine={settings.ocr_engine}, max_pages={settings.ocr_max_pages}", flush=True)
    
    result = run_ocr(imgs, settings=settings)
    print(f"\nSuccess! Extracted {len(result)} characters", flush=True)
    print(f"\nFirst 500 chars:\n{result[:500]}", flush=True)
except Exception as e:
    print(f"   ERROR: {type(e).__name__}: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
