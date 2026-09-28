from pathlib import Path

from pypdf import PdfReader

def parse_pdf_pages(file_path: Path) -> list[dict]:
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            pages.append(
                {
                    "page": page_number,
                    "text": text
                }
            )

    return pages


def parse_text_file(file_path: Path) -> list[dict]:
    text = file_path.read_text(encoding="utf-8")

    return [
        {
            "page": None,
            "text": text
        }
    ]

def parse_document(file_path: Path) -> list[dict]:
    extension = file_path.suffix.lower()
    if extension == ".pdf":
        return parse_pdf_pages(file_path)
    if extension in {".txt", ".md"}:
        return parse_text_file(file_path)
    raise ValueError(
        f"Unsupported file type: {extension}"
    )


































