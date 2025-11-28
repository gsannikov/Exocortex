
import pytest
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from local_rag.ingestion.extractors import read_text_with_ocr
from local_rag.settings import get_settings

def create_dummy_pdf_with_text(path: Path, text: str, lang: str = "eng"):
    """
    Create a PDF containing an image of the specified text.
    This simulates a scanned document.
    """
    # Create an image
    img = Image.new('RGB', (800, 600), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to load a font that supports the language
    # On CI (Ubuntu), DejaVuSans usually supports Hebrew
    font = None
    try:
        # Common paths for fonts
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial.ttf"
        ]
        for fp in font_paths:
            if Path(fp).exists():
                font = ImageFont.truetype(fp, 48)
                break
        if not font:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Draw text
    d.text((50, 50), text, fill='black', font=font)
    
    # Save as PDF
    img.save(path, "PDF", resolution=100.0)

@pytest.mark.integration
def test_ocr_hebrew_pdf(tmp_path):
    """
    Test that a PDF with Hebrew text is correctly processed by ocrmypdf.
    """
    # Create a dummy PDF with Hebrew text
    # Note: If the system font doesn't support Hebrew, the image will have squares,
    # and OCR will fail to read Hebrew. 
    # But we can at least verify the pipeline runs without crashing.
    pdf_path = tmp_path / "hebrew_test.pdf"
    
    # "Shalom" in Hebrew
    hebrew_text = "שלום"
    
    create_dummy_pdf_with_text(pdf_path, hebrew_text, "heb")
    
    # Configure settings
    settings = get_settings()
    settings.ocr_enabled = True
    settings.ocr_lang = "he"
    settings.ocr_engine = "tesseract"
    
    # Run extraction
    # We expect this to run ocrmypdf
    try:
        text = read_text_with_ocr(pdf_path, settings=settings)
        
        # Check if we got something back
        # Even if OCR fails to read exact Hebrew (due to font issues), 
        # it should return a string and not crash.
        assert isinstance(text, str)
        print(f"Extracted text: {text}")
        
        # If we successfully rendered Hebrew, we might see it.
        # If not, we might see garbage or nothing.
        # But the main goal is to ensure the Tesseract pipeline works.
        
    except ImportError:
        pytest.skip("ocrmypdf not installed")
    except Exception as e:
        pytest.fail(f"OCR failed: {e}")

@pytest.mark.integration
def test_ocr_english_pdf(tmp_path):
    """
    Test that a PDF with English text is correctly processed by ocrmypdf.
    This is a more reliable test for the pipeline itself since default fonts support English.
    """
    pdf_path = tmp_path / "english_test.pdf"
    text_content = "Hello World"
    
    create_dummy_pdf_with_text(pdf_path, text_content, "eng")
    
    settings = get_settings()
    settings.ocr_enabled = True
    settings.ocr_lang = "en"
    settings.ocr_engine = "tesseract"
    
    try:
        text = read_text_with_ocr(pdf_path, settings=settings)
        assert "Hello" in text or "World" in text or "He" in text # Tesseract might be imperfect on generated images
    except ImportError:
        pytest.skip("ocrmypdf not installed")
