import json
import subprocess
from pathlib import Path
from backend.utils import get_models_dir, get_base_dir
from backend.models.metadata import load_metadata, save_metadata, update_last_used

CONFIG_PATH = get_base_dir() / "backend" / "config" / "model_config.json"

def list_installed_models() -> list:
    """
    Uses Ollama to list installed models.
    """
    try:
        result = subprocess.run(
            ["ollama", "list", "--json"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return []

        models = []
        for line in result.stdout.splitlines():
            entry = json.loads(line)
            name = entry["name"]
            meta = load_metadata(name)

            models.append({
                "name": name,
                "size_mb": entry.get("size", None),
                "installed": True,
                "last_used": meta.get("last_used"),
            })
        return models

    except Exception:
        return []

def delete_model(model_name: str) -> bool:
    """
    Deletes a model via Ollama.
    """
    try:
        subprocess.run(["ollama", "rm", model_name])
    except Exception:
        return False

    # Remove metadata
    meta_path = get_models_dir() / f"{model_name}.meta.json"
    if meta_path.exists():
        meta_path.unlink()

    return True

def set_active_model(model_name: str):
    data = {"active_model": model_name}
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)
    update_last_used(model_name)

def get_active_model() -> str | None:
    if not CONFIG_PATH.exists():
        return None
    with open(CONFIG_PATH, "r") as f:
        return json.load(f).get("active_model")

def speed_test(model_name: str) -> dict:
    """
    Runs a short benchmark using Ollama.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, "Hello"],
            capture_output=True,
            text=True
        )
        # Ollama does not expose tokens/sec directly.
        # You can parse logs or implement a custom test later.
        return {
            "name": model_name,
            "tokens_per_second": None,
            "raw_output": result.stdout
        }
    except Exception as e:
        return {"error": str(e)}
