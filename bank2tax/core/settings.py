import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    # Paths
    project_root: Path
    data_dir: Path
    output_dir: Path

    # Ollama
    ollama_base_url: str
    ollama_model: str
    ollama_temperature: float
    ollama_timeout_s: float

    # Output
    save_md: int


def load_settings() -> Settings:
    # bank2tax/bank2tax/app/settings.py -> project root is two levels up
    project_root = Path(__file__).resolve().parents[2]

    # Load .env if present
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    return Settings(
        project_root=project_root,
        data_dir=Path(os.getenv("BANK2TAX_DATA_DIR", str(project_root / "data"))),
        output_dir=Path(os.getenv("BANK2TAX_OUTPUT_DIR", str(project_root / "output"))),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "mistral:7b"),
        ollama_temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0.0")),
        ollama_timeout_s=float(os.getenv("OLLAMA_TIMEOUT_S", "120")),
        save_md=int(os.getenv("SAVE_MD", "0")),
    )
