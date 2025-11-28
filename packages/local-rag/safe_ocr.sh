#!/bin/bash
# Safe OCR wrapper for problematic PDFs
# Uses ocrmypdf (Tesseract) instead of PaddleOCR

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <input.pdf> <output.pdf>"
    echo ""
    echo "Safely OCRs a PDF using Tesseract instead of PaddleOCR"
    echo ""
    echo "Prerequisites:"
    echo "  brew install ocrmypdf"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file not found: $INPUT"
    exit 1
fi

echo "🔍 Processing: $INPUT"
echo "📄 Output: $OUTPUT"
echo ""

# Check if ocrmypdf is installed
if ! command -v ocrmypdf &> /dev/null; then
    echo "❌ ocrmypdf not found. Install with:"
    echo "   brew install ocrmypdf"
    exit 1
fi

# Run OCR with Tesseract (safe alternative to PaddleOCR)
echo "🚀 Running OCR with Tesseract..."
ocrmypdf \
    --force-ocr \
    --optimize 1 \
    --output-type pdf \
    --language eng+heb \
    "$INPUT" \
    "$OUTPUT"

echo "✅ Done! OCR'd PDF saved to: $OUTPUT"
echo ""
echo "Now you can index it with:"
echo "  OCR_ENABLED=false python3 indexer.py \"$OUTPUT\""
