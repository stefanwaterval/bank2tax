import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    # Paths
    project_root: Path
    data_dir: Path
    output_dir: Path

    # Ollama
    ollama_base_url: str
    ollama_model: str
    ollama_timeout_s: float


def load_settings() -> Settings:
    # bank2tax/bank2tax/app/settings.py -> project root is two levels up
    project_root = Path(__file__).resolve().parents[2]

    data_dir = Path(os.getenv("BANK2TAX_DATA_DIR", str(project_root / "data")))
    output_dir = Path(os.getenv("BANK2TAX_OUTPUT_DIR", str(project_root / "output")))

    return Settings(
        project_root=project_root,
        data_dir=data_dir,
        output_dir=output_dir,
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
        ollama_timeout_s=float(os.getenv("OLLAMA_TIMEOUT_S", "120")),
    )
