from pathlib import Path

from docling.document_converter import DocumentConverter

_converter = DocumentConverter()


def pdf_to_markdown(pdf_path: str | Path) -> str:
    """Convert a PDF file to a Markdown string using Docling.

    Args:
        pdf_path: Path to the input PDF file.
    """
    pdf_path = Path(pdf_path)

    result = _converter.convert(pdf_path)
    document = result.document

    markdown = document.export_to_markdown()

    return markdown
