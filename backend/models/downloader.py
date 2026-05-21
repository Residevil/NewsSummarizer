import subprocess
from pathlib import Path
from backend.utils import get_models_dir
from backend.models.metadata import save_metadata

def download_with_ollama(model_name: str) -> bool:
    """
    Downloads a model using Ollama.
    """
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("Ollama error:", result.stderr)
            return False
        return True
    except Exception as e:
        print("Download error:", e)
        return False

def register_download(model_name: str):
    """
    After download, register metadata.
    """
    models_dir = get_models_dir()

    # Ollama stores models in ~/.ollama/models
    # We only store metadata, not the actual file
    meta = {
        "name": model_name,
        "installed": True,
        "path": str(models_dir),
        "size_mb": None,  # optional
        "last_used": None
    }
    save_metadata(model_name, meta)

def download_model(model_name: str) -> bool:
    ok = download_with_ollama(model_name)
    if ok:
        register_download(model_name)
    return ok
