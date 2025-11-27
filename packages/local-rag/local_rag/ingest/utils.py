from pathlib import Path

def is_allowed(p: Path, allowed_exts: set[str]) -> bool:
    return p.is_file() and p.suffix.lower() in allowed_exts
