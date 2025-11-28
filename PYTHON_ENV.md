# Python Environment Setup

This repository only has one Python-heavy skill: **local-rag**. These steps set up a clean, reproducible environment that works across macOS and Ubuntu while avoiding wheel issues seen on newer Python versions.

## 1) Use Python 3.11 (recommended)
- Verified version: **3.11.14**
- Avoid 3.14 for now (onnxruntime/ocrmypdf wheels are not reliable there).
- Install via pyenv:
  ```bash
  brew install pyenv                     # macOS
  pyenv install 3.11.14
  pyenv local 3.11.14
  ```

## 2) Remove old virtualenvs
If you have legacy environments in this repo:
```bash
rm -rf .venv .venv311 .venv_ocr
```

## 3) Create a fresh virtualenv
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
```

## 4) Install system packages (Local RAG OCR)
macOS:
```bash
brew install tesseract qpdf ghostscript poppler antiword
```
Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-heb qpdf ghostscript poppler-utils antiword
```

## 5) Install Python dependencies
```bash
pip install -r packages/local-rag/requirements-dev.txt
```

## 6) Verify everything
```bash
LOCAL_RAG_REAL_OCR_DEPS=1 pytest packages/local-rag/tests -q
```
Expected: 149 tests passing.

## Tips
- Keep the `.venv` out of git (already ignored).
- If you need GPU/TensorRT builds, install those separately, but the default CPU stack above is what CI uses.
- If you swap Python versions, recreate the virtualenv—don’t reuse it across major/minor versions.
