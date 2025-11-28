FROM python:3.11-slim

# Install system dependencies
# build-essential: for compiling python extensions
# poppler-utils: for pdf2image
# tesseract-ocr: for OCR
# libgl1: for opencv/paddle (if needed)
# libgomp1: for paddle
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage cache
COPY requirements.txt .

# Install dependencies
# Note: We don't need the HNSWLIB_NO_NATIVE workaround here because 
# we are on Linux (Debian) in the container, where wheels usually exist or build fine.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the package
COPY . .

# Install the package in editable mode (or just install it)
RUN pip install -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OCR_ENABLED=true

# Entrypoint runs the MCP server
ENTRYPOINT ["python", "-m", "local_rag.mcp"]
