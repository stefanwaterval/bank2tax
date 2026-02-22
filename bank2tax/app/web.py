import asyncio
from pathlib import Path
from time import perf_counter

from nicegui import run, ui
from nicegui.events import UploadEventArguments

from bank2tax.core.extractor import ExtractorAgent
from bank2tax.core.ollama_client import OllamaClient
from bank2tax.core.pipeline import run_pipeline
from bank2tax.core.settings import load_settings


def main() -> None:
    settings = load_settings()

    output_dir = settings.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_dir = settings.project_root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

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

    async def save_upload(event: UploadEventArguments) -> None:
        filename = Path(event.file.name).name
        dest = temp_dir / filename

        await event.file.save(dest)

    ui.upload(
        label="Upload PDFs",
        multiple=True,
        auto_upload=True,
        on_upload=save_upload,
    ).props('accept=".pdf"')
    run_btn = ui.button("Run extraction", icon="play_arrow")
    spinner = ui.spinner(size="lg").classes("text-gray-500")
    spinner.visible = False

    async def on_run() -> None:
        error_label.text = ""
        latency_label.text = ""
        spinner.visible = True
        run_btn.disable()

        await asyncio.sleep(0)

        try:
            pdf_paths = sorted(temp_dir.glob("*.pdf"))
            source_dir = temp_dir

            if not pdf_paths:
                raise FileNotFoundError(f"No PDF found in {source_dir}")

            t0 = perf_counter()

            result = await run.io_bound(
                run_pipeline,
                pdf_paths=pdf_paths,
                extractor=extractor,
                output_dir=output_dir,
                save_md=0,
            )

            t1 = perf_counter()

            table.rows = result.to_table_rows()
            table.update()

            latency_label.text = (
                f"Latency: {t1 - t0:.2f} seconds | PDFs processed: {len(pdf_paths)}"
            )

        except Exception as e:
            error_label.text = f"Error: {type(e).__name__}: {e}"

        finally:
            spinner.visible = False
            run_btn.enable()

            # Clean up temp_dir
            for uploaded_pdf in temp_dir.glob("*.pdf"):
                try:
                    uploaded_pdf.unlink()
                except Exception:
                    pass

    run_btn.on_click(on_run)

    ui.run(title="bank2tax", reload=False, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
