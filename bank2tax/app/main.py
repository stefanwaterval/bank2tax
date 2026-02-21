from __future__ import annotations

import asyncio
from time import perf_counter
from typing import Any

from nicegui import run, ui

from bank2tax.core.extractor import ExtractorAgent
from bank2tax.core.ollama_client import OllamaClient
from bank2tax.core.pipeline import run_pipeline
from bank2tax.core.settings import load_settings


def main() -> None:
    settings = load_settings()

    output_dir = settings.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    client = OllamaClient(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
        temperature=settings.ollama_temperature,
        timeout_s=settings.ollama_timeout_s,
    )
    extractor = ExtractorAgent(client)

    ui.page_title("bank2tax")

    latency_label = ui.label("").classes("text-sm text-gray-600")
    error_label = ui.label("").classes("text-sm text-red-600")

    table = ui.table(
        columns=[
            {
                "name": "source_file",
                "label": "Source file",
                "field": "source_file",
                "align": "left",
            },
            {
                "name": "institution",
                "label": "Institution",
                "field": "institution",
                "align": "left",
            },
            {
                "name": "account_number",
                "label": "Account No",
                "field": "account_number",
                "align": "left",
            },
            {
                "name": "ending_balance",
                "label": "Ending balance",
                "field": "ending_balance",
                "align": "right",
            },
            {
                "name": "currency",
                "label": "Currency",
                "field": "currency",
                "align": "left",
            },
        ],
        rows=[],
        row_key="row_id",
        pagination=10,
    ).classes("w-full")

    run_btn = ui.button("Run extraction", icon="play_arrow")
    spinner = ui.spinner(size="lg").classes("text-gray-500")
    spinner.visible = False

    def _build_rows(result: Any) -> list[dict[str, Any]]:
        # Attach source_file to each account row for display.
        rows: list[dict[str, Any]] = []
        row_id = 0
        for doc in result.documents:
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

    async def on_run() -> None:
        error_label.text = ""
        latency_label.text = ""
        spinner.visible = True
        run_btn.disable()

        await asyncio.sleep(0)

        try:
            pdf_paths = sorted(settings.data_dir.glob("*.pdf"))
            if not pdf_paths:
                raise FileNotFoundError(f"No PDF found in {settings.data_dir}")

            t0 = perf_counter()

            result = await run.io_bound(
                run_pipeline,
                pdf_paths=pdf_paths,
                extractor=extractor,
                output_dir=output_dir,
                save_md=settings.save_md,
            )

            t1 = perf_counter()

            table.rows = _build_rows(result)
            table.update()

            latency_label.text = (
                f"Latency: {t1 - t0:.2f} seconds | PDFs processed: {len(pdf_paths)}"
            )

        except Exception as e:
            error_label.text = f"Error: {type(e).__name__}: {e}"

        finally:
            spinner.visible = False
            run_btn.enable()

    run_btn.on_click(on_run)

    ui.separator()
    ui.markdown(
        "- Put PDFs into your configured `data_dir` and click **Run extraction**.\n"
    ).classes("text-sm text-gray-600")

    ui.run(title="bank2tax", reload=False, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
