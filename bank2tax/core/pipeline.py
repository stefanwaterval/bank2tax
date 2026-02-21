from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from bank2tax.core.docling_io import pdf_to_markdown
from bank2tax.core.extractor import ExtractorAgent
from bank2tax.core.schema import ExtractedAccount, ExtractedDocument


@dataclass(frozen=True)
class PipelineResult:
    documents: list[ExtractedDocument]
    accounts: list[ExtractedAccount]


def run_pipeline(
    pdf_paths: Iterable[str | Path],
    extractor: ExtractorAgent,
) -> PipelineResult:
    documents: list[ExtractedDocument] = []
    accounts: list[ExtractedAccount] = []

    for p in pdf_paths:
        path = Path(p)
        markdown = pdf_to_markdown(path)

        raw = extractor.extract(markdown=markdown, source_file=path.name)
        doc = ExtractedDocument.model_validate_json(raw)

        documents.append(doc)
        accounts.extend(doc.accounts)

        documents.append(doc)
        accounts.extend(doc.accounts)

    return PipelineResult(documents=documents, accounts=accounts)
