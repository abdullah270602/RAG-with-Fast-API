from abc import ABC, abstractmethod
import io
import logging
from PIL import Image
import PyPDF2
import pytesseract
import fitz  # PyMuPDF


# Base parser interface
class BaseParser(ABC):
    @abstractmethod
    def parse(self, filepath: str) -> str:
        """Abstract method to parse file content."""
        pass

# Concrete Parser for TXT Files
class TxtParser(BaseParser):
    def parse(self, filepath: str) -> str:
        """Parses a text file and returns its content."""
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except Exception as e:
            logging.error(f"Error reading text file: {e}")
            return "Error reading text file"


class PdfParser(BaseParser):
    def parse(self, filepath: str) -> str:
        try:
            content: str = ""
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if reader.is_encrypted:
                    try:
                        reader.decrypt('')
                    except Exception as e:
                        logging.error(f"Failed to decrypt PDF: {e}")
                        return "Unable to decrypt PDF"

                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    page_content = page.extract_text()
                    if not page_content:  # If text extraction fails, use OCR
                        page_content = self._ocr_page(filepath, page_num)
                    content += page_content
            return content
        except Exception as e:
            logging.error(f"Error processing PDF: {e}")
            return "Error processing PDF file"

    def _ocr_page(self, filepath: str, page_num: int) -> str:
        try:
            document = fitz.open(filepath)
            page = document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            document.close()
            return ocr_text
        except Exception as e:
            logging.error(f"OCR processing error: {e}")
            return "Error in OCR processing"