import os
import io
import base64
import hashlib
import logging
from pathlib import Path
from typing import List, Optional, Any

import requests
from PIL import Image

from ..settings import LocalRagSettings, get_settings

logger = logging.getLogger(__name__)

# Cached defaults for backward compatibility with tests/env monkeypatching
_DEFAULT_SETTINGS = get_settings()
ENGINE = (_DEFAULT_SETTINGS.ocr_engine or "tesseract").lower()
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


def _resolve_tesseract_lang(lang_spec: Optional[str]) -> str:
    """
    Map human-friendly language codes to Tesseract codes and support multiple languages.
    
    Accepts comma- or plus-separated inputs (e.g., "en,he" or "eng+heb") and
    normalizes them for pytesseract/ocrmypdf.
    """
    if not lang_spec:
        return "eng"

    lang_map = {
        "he": "heb",
        "hebrew": "heb",
        "en": "eng",
        "english": "eng",
    }

    parts = [p.strip() for p in lang_spec.replace("+", ",").split(",") if p.strip()]
    if not parts:
        return "eng"

    mapped = [lang_map.get(p.lower(), p) for p in parts]
    return "+".join(mapped)

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
    try:
        import pytesseract
    except ImportError as exc:
        raise RuntimeError("pytesseract is required for Tesseract OCR. Install with `pip install pytesseract`.") from exc

    cache_dir = _get_cache_dir(settings)
    
    tess_lang = _resolve_tesseract_lang(settings.ocr_lang)
    
    texts = []
    for idx, im in enumerate(images, 1):
        try:
            logger.info(f"OCR: Processing image {idx}/{len(images)}...")
            h = _img_sha(im)
            hit = _cache_get(h, cache_dir)
            if hit is not None:
                logger.debug(f"OCR: Image {idx} - cache hit")
                texts.append(hit)
                continue

            logger.debug(f"OCR: Image {idx} - running Tesseract...")
            txt = pytesseract.image_to_string(im, lang=tess_lang)
            logger.debug(f"OCR: Image {idx} - extracted {len(txt)} chars")
            _cache_put(h, txt, cache_dir)
            texts.append(txt)
        except Exception as exc:
            logger.warning(f"Warning: Tesseract failed on image {idx}: {exc}")
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
    engine = (settings.ocr_engine or globals().get("ENGINE") or "tesseract").lower()
    if engine in {"noop", "none", "off", "disable"}:
        return ""
    if engine == "surya":
        return ocr_surya(images, settings)
    if engine == "paddle":
        logger.warning("Warning: PaddleOCR support removed; falling back to Tesseract.")
        return ocr_tesseract(images, settings)
    if engine == "tesseract":
        return ocr_tesseract(images, settings)
    if engine == "deepseek":
        return ocr_deepseek(images, settings)
    return ocr_tesseract(images, settings)
