from pathlib import Path
import fitz
from docx import Document

class DocumentParser:
    """
    Extracts text from supported document formats
    """
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Detect file type and extract text
        """
        extension=Path(file_path).suffix.lower()

        if extension == ".pdf":
            return DocumentParser.extract_pdf(file_path)

        elif extension == ".docx":
            return DocumentParser.extract_docx(file_path)

        elif extension == ".txt":
            return DocumentParser.extract_txt(file_path)

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

    @staticmethod
    def extract_pdf(file_path: str) -> str:
        """
        extract text from pdf
        """
        text = ""
        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()
        pdf.close()
        return text
    @staticmethod
    def extract_docx(file_path: str) -> str:
        """
        Extract text from Docx
        """
        document = Document(file_path)
        text=[]
        for paragraph in document.paragraphs:
            text.append(paragraph.text)

        return "\n".join(text)
    @staticmethod
    def extract_txt(file_path: str) -> str:
        """
        extract text from text file
        """
        with open(
            file_path,
            "r",
            encoding="utf-8"
        )as file:
            return file.read()
        