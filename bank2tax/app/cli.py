from time import perf_counter

from bank2tax.core.extractor import ExtractorAgent
from bank2tax.core.ollama_client import OllamaClient
from bank2tax.core.pipeline import run_pipeline
from bank2tax.core.settings import load_settings


def main() -> None:
    settings = load_settings()

    output_dir = settings.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    data_dir = settings.data_dir

    client = OllamaClient(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
        temperature=settings.ollama_temperature,
        timeout_s=settings.ollama_timeout_s,
    )
    extractor = ExtractorAgent(client)

    try:
        pdf_paths = sorted(data_dir.glob("*.pdf"))
        source_dir = data_dir

        if not pdf_paths:
            raise FileNotFoundError(f"No PDF found in {source_dir}")

        t0 = perf_counter()

        result = run_pipeline(
            pdf_paths=pdf_paths,
            extractor=extractor,
            output_dir=output_dir,
            save_md=settings.save_md,
        )

        t1 = perf_counter()

        print("\n===== RESULT =====\n")
        for doc in result.documents:
            print(doc.model_dump_json(indent=2))
        print(f"\nLatency: {t1 - t0:.3f} s")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
