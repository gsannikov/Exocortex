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
ENGINE = (_DEFAULT_SETTINGS.ocr_engine or "paddle").lower()
OCR_LANG = _DEFAULT_SETTINGS.ocr_lang
CACHE_DIR = None  # Populated lazily
_PADDLE_CLIENT = None
_PADDLE_LANG = None
_PADDLE_LOCK = threading.Lock()

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

def ocr_paddle(images: List[Any], settings: LocalRagSettings) -> str:
    from paddleocr import PaddleOCR
    import numpy as np
    cache_dir = _get_cache_dir(settings)

    # Parse language config - PaddleOCR uses specific lang codes
    # For Hebrew, we use 'ar' (Arabic) as it shares RTL characteristics
    # or 'latin' for mixed content. 'multilingual' also works.
    lang = settings.ocr_lang.split(',')[0].strip() if ',' not in settings.ocr_lang else 'en'

    # Map common language codes to PaddleOCR codes
    lang_map = {
        'he': 'ar',      # Hebrew -> use Arabic model (RTL support)
        'hebrew': 'ar',
        'en': 'en',
        'english': 'en',
        'multi': 'en',   # Multilingual fallback
    }
    paddle_lang = lang_map.get(lang.lower(), lang)

    # Some PaddleOCR versions don't support show_log; fall back gracefully.
    global _PADDLE_CLIENT, _PADDLE_LANG
    with _PADDLE_LOCK:
        if _PADDLE_CLIENT is None or _PADDLE_LANG != paddle_lang:
            try:
                _PADDLE_CLIENT = PaddleOCR(use_angle_cls=True, lang=paddle_lang, show_log=False)
            except Exception as exc:
                if "show_log" in str(exc):
                    _PADDLE_CLIENT = PaddleOCR(use_angle_cls=True, lang=paddle_lang)
                else:
                    raise
            _PADDLE_LANG = paddle_lang
        ocr = _PADDLE_CLIENT
    texts = []
    for im in images:
        try:
            h = _img_sha(im)
            hit = _cache_get(h, cache_dir)
            if hit is not None:
                texts.append(hit)
                continue
            # Convert PIL Image to numpy array for PaddleOCR
            img_array = np.array(im)
            # Some Paddle versions don't accept cls kwarg; retry without it.
            try:
                res = ocr.ocr(img_array, cls=True)
            except TypeError as exc:
                if "cls" in str(exc):
                    res = ocr.ocr(img_array)
                else:
                    raise
            txt = "\n".join([line[1][0] for line in (res[0] or [])])
            _cache_put(h, txt, cache_dir)
            texts.append(txt)
        except Exception as exc:
            # Bail out gracefully if Paddle throws lower-level runtime errors
            print(f"Warning: PaddleOCR failed on image: {exc}")
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
    engine = (globals().get("ENGINE") or settings.ocr_engine or "paddle").lower()
    if engine == "surya":
        return ocr_surya(images, settings)
    if engine == "paddle":
        return ocr_paddle(images, settings)
    if engine == "deepseek":
        return ocr_deepseek(images, settings)
    return ""
