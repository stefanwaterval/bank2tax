from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from bank2tax.core.docling_io import pdf_to_markdown
from bank2tax.core.extractor import ExtractorAgent
from bank2tax.core.schema import ExtractedAccount, ExtractedDocument


@dataclass(frozen=True)
class PipelineResult:
    """Container for structured extraction results."""

    documents: list[ExtractedDocument]
    accounts: list[ExtractedAccount]

    def to_table_rows(self) -> list[dict[str, Any]]:
        """Flatten extracted data into row-oriented dictionaries."""
        rows = []
        row_id = 0
        for doc in self.documents:
            for acc in doc.accounts:
                row_id += 1
                rows.append(
                    {
                        "row_id": row_id,
                        "source_file": doc.source_file,
                        "institution": acc.institution,
                        "currency": acc.currency,
                        "ending_balance": acc.ending_balance,
                        "account_number": acc.account_number,
                    }
                )

        return rows


def run_pipeline(
    pdf_paths: Iterable[str | Path],
    extractor: ExtractorAgent,
    output_dir: Path,
    save_md: int = 0,
) -> PipelineResult:
    """Run the full extraction pipeline on a collection of PDFs.

    Args:
        pdf_paths: Paths to input PDF files.
        extractor: Agent used to extract structured data.
        output_dir: Directory where outputs are written.
        save_md: Whether to save intermediate Markdown files (1 to enable).
    """
    documents: list[ExtractedDocument] = []
    accounts: list[ExtractedAccount] = []

    for p in pdf_paths:
        path = Path(p)
        markdown = pdf_to_markdown(path)

        if save_md == 1:
            md_file = output_dir / f"{path.stem}.md"
            md_file.write_text(markdown, encoding="utf-8")

        raw = extractor.extract(markdown=markdown, source_file=path.name)
        doc = ExtractedDocument.model_validate_json(raw)

        documents.append(doc)
        accounts.extend(doc.accounts)

    return PipelineResult(documents=documents, accounts=accounts)
