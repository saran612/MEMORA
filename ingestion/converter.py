import fitz  # PyMuPDF
from pathlib import Path
from config.settings import settings
import os

class Converter:
    @staticmethod
    def to_markdown(file_path: Path):
        """
        Converts file to markdown and saves it in DATA_PROCESSED_DIR.
        """
        ext = file_path.suffix.lower()
        processed_file = settings.DATA_PROCESSED_DIR / f"{file_path.stem}.md"
        
        content = ""
        if ext == ".pdf":
            content = Converter._pdf_to_text(file_path)
        elif ext == ".txt":
            content = Converter._txt_to_text(file_path)
        elif ext == ".md":
            # Just copy it
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        with open(processed_file, "w", encoding="utf-8") as f:
            f.write(content)
            
        return processed_file

    @staticmethod
    def _pdf_to_text(file_path: Path):
        doc = fitz.open(str(file_path))
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    @staticmethod
    def _txt_to_text(file_path: Path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

converter = Converter()
