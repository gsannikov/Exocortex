import os
import io
import base64
import hashlib
import threading
from pathlib import Path
from typing import List, Optional, Any

import requests
from PIL import Image

from ..settings import LocalRagSettings, get_settings

# Cached defaults for backward compatibility with tests/env monkeypatching
_DEFAULT_SETTINGS = get_settings()
ENGINE = (_DEFAULT_SETTINGS.ocr_engine or "tesseract").lower()
OCR_LANG = _DEFAULT_SETTINGS.ocr_lang
CACHE_DIR = None  # Populated lazily

def _img_sha(img: Any) -> str:
    b = io.BytesIO()
    img.save(b, format="PNG")
    data = b.getvalue()
    return hashlib.sha1(data).hexdigest()

def _get_cache_dir(settings: Optional[LocalRagSettings] = None) -> Path:
    global CACHE_DIR
    if CACHE_DIR is not None:
        return CACHE_DIR
    settings = settings or _DEFAULT_SETTINGS
    default_dir = Path.home() / ".cache" / "local-rag" / "ocr_cache"
    cache_dir = settings.ocr_cache_dir or default_dir
    cache_dir.mkdir(parents=True, exist_ok=True)
    CACHE_DIR = cache_dir
    return cache_dir

def _cache_get(h: str, cache_dir: Optional[Path] = None):
    cache_dir = cache_dir or _get_cache_dir()
    p = cache_dir / f"{h}.txt"
    return p.read_text() if p.exists() else None


def _cache_put(h: str, txt: str, cache_dir: Optional[Path] = None):
    cache_dir = cache_dir or _get_cache_dir()
    (cache_dir / f"{h}.txt").write_text(txt)

def ocr_surya(images: List[Any], settings: LocalRagSettings) -> str:
    from surya.ocr import run_ocr
    import numpy as np
    cache_dir = _get_cache_dir(settings)
    texts=[]
    for im in images:
        h=_img_sha(im)
        hit=_cache_get(h, cache_dir)
        if hit is not None:
            texts.append(hit)
            continue
        out = run_ocr([np.array(im)])
        txt = "\n".join(block["text"] for page in out for block in page["text_blocks"])
        _cache_put(h, txt, cache_dir)
        texts.append(txt)
    return "\n\f\n".join(texts)

def ocr_tesseract(images: List[Any], settings: LocalRagSettings) -> str:
    import pytesseract
    cache_dir = _get_cache_dir(settings)
    
    # Map languages
    lang = settings.ocr_lang.split(',')[0].strip() if ',' not in settings.ocr_lang else 'eng'
    lang_map = {
        'he': 'heb',
        'hebrew': 'heb',
        'en': 'eng',
        'english': 'eng',
    }
    tess_lang = lang_map.get(lang.lower(), lang)
    
    texts = []
    for idx, im in enumerate(images, 1):
        try:
            print(f"OCR: Processing image {idx}/{len(images)}...", flush=True)
            h = _img_sha(im)
            hit = _cache_get(h, cache_dir)
            if hit is not None:
                print(f"OCR: Image {idx} - cache hit", flush=True)
                texts.append(hit)
                continue
                
            print(f"OCR: Image {idx} - running Tesseract...", flush=True)
            txt = pytesseract.image_to_string(im, lang=tess_lang)
            print(f"OCR: Image {idx} - extracted {len(txt)} chars", flush=True)
            _cache_put(h, txt, cache_dir)
            texts.append(txt)
        except Exception as exc:
            print(f"Warning: Tesseract failed on image {idx}: {exc}", flush=True)
            texts.append("")
            
    return "\n\f\n".join(texts)

def ocr_deepseek(images: List[Any], settings: LocalRagSettings) -> str:
    cache_dir = _get_cache_dir(settings)
    url = os.getenv("DEEPSEEK_OCR_URL")
    model = os.getenv("DEEPSEEK_OCR_MODEL")
    texts=[]
    for im in images:
        h=_img_sha(im)
        hit=_cache_get(h, cache_dir)
        if hit is not None:
            texts.append(hit)
            continue
        b = io.BytesIO()
        im.save(b, format="PNG")
        payload = {"model": model, "prompt": "", "images": [base64.b64encode(b.getvalue()).decode()], "temperature": 0.0, "max_tokens": 4096}
        data = requests.post(url, json=payload, timeout=120).json()
        txt = data.get("choices",[{}])[0].get("text","")
        _cache_put(h, txt, cache_dir)
        texts.append(txt)
    return "\n\f\n".join(texts)

def run_ocr(images: List[Any], settings: Optional[LocalRagSettings] = None) -> str:
    settings = settings or get_settings()
    if not images:
        return ""
    engine = (globals().get("ENGINE") or settings.ocr_engine or "tesseract").lower()
    if engine in {"noop", "none", "off", "disable"}:
        return ""
    if engine == "surya":
        return ocr_surya(images, settings)
    if engine == "paddle":
        # Fallback to tesseract if paddle requested but removed
        return ocr_tesseract(images, settings)
    if engine == "tesseract":
        return ocr_tesseract(images, settings)
    if engine == "deepseek":
        return ocr_deepseek(images, settings)
    return ocr_tesseract(images, settings)
