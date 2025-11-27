import os
import io
import base64
import hashlib

import requests
from pathlib import Path
from typing import List
from PIL import Image

ENGINE = os.getenv("OCR_ENGINE", "paddle").lower()
OCR_LANG = os.getenv("OCR_LANG", "en,he")  # Default: English + Hebrew

_default_cache_dir = Path.home() / ".cache" / "local-rag" / "ocr_cache"
CACHE_DIR = Path(os.getenv("OCR_CACHE_DIR", _default_cache_dir))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _img_sha(img: Image.Image) -> str:
    b = io.BytesIO()
    img.save(b, format="PNG")
    data = b.getvalue()
    return hashlib.sha1(data).hexdigest()

def _cache_get(h): 
    p = CACHE_DIR / f"{h}.txt"
    return p.read_text() if p.exists() else None

def _cache_put(h, txt): 
    (CACHE_DIR / f"{h}.txt").write_text(txt)

def ocr_surya(images: List[Image.Image]) -> str:
    from surya.ocr import run_ocr
    import numpy as np
    texts=[]
    for im in images:
        h=_img_sha(im)
        hit=_cache_get(h)
        if hit is not None:
            texts.append(hit)
            continue
        out = run_ocr([np.array(im)])
        txt = "\n".join(block["text"] for page in out for block in page["text_blocks"])
        _cache_put(h, txt)
        texts.append(txt)
    return "\n\f\n".join(texts)

def ocr_paddle(images: List[Image.Image]) -> str:
    from paddleocr import PaddleOCR
    import numpy as np

    # Parse language config - PaddleOCR uses specific lang codes
    # For Hebrew, we use 'ar' (Arabic) as it shares RTL characteristics
    # or 'latin' for mixed content. 'multilingual' also works.
    lang = OCR_LANG.split(',')[0].strip() if ',' not in OCR_LANG else 'en'

    # Map common language codes to PaddleOCR codes
    lang_map = {
        'he': 'ar',      # Hebrew -> use Arabic model (RTL support)
        'hebrew': 'ar',
        'en': 'en',
        'english': 'en',
        'multi': 'en',   # Multilingual fallback
    }
    paddle_lang = lang_map.get(lang.lower(), lang)

    ocr = PaddleOCR(use_angle_cls=True, lang=paddle_lang, show_log=False)
    texts = []
    for im in images:
        h = _img_sha(im)
        hit = _cache_get(h)
        if hit is not None:
            texts.append(hit)
            continue
        # Convert PIL Image to numpy array for PaddleOCR
        img_array = np.array(im)
        res = ocr.ocr(img_array, cls=True)
        txt = "\n".join([line[1][0] for line in (res[0] or [])])
        _cache_put(h, txt)
        texts.append(txt)
    return "\n\f\n".join(texts)

def ocr_deepseek(images: List[Image.Image]) -> str:
    url = os.getenv("DEEPSEEK_OCR_URL")
    model = os.getenv("DEEPSEEK_OCR_MODEL")
    texts=[]
    for im in images:
        h=_img_sha(im)
        hit=_cache_get(h)
        if hit is not None:
            texts.append(hit)
            continue
        b = io.BytesIO()
        im.save(b, format="PNG")
        payload = {"model": model, "prompt": "", "images": [base64.b64encode(b.getvalue()).decode()], "temperature": 0.0, "max_tokens": 4096}
        data = requests.post(url, json=payload, timeout=120).json()
        txt = data.get("choices",[{}])[0].get("text","")
        _cache_put(h, txt)
        texts.append(txt)
    return "\n\f\n".join(texts)

def run_ocr(images: List[Image.Image]) -> str:
    if ENGINE == "surya":
        return ocr_surya(images)
    if ENGINE == "paddle":
        return ocr_paddle(images)
    if ENGINE == "deepseek":
        return ocr_deepseek(images)
    return ""
