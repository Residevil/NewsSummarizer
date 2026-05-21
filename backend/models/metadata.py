import json
from pathlib import Path
from datetime import datetime
from backend.utils import get_models_dir

def get_metadata_path(model_name: str) -> Path:
    models_dir = get_models_dir()
    return models_dir / f"{model_name}.meta.json"

def load_metadata(model_name: str) -> dict:
    meta_path = get_metadata_path(model_name)
    if not meta_path.exists():
        return {}
    with open(meta_path, "r") as f:
        return json.load(f)

def save_metadata(model_name: str, data: dict):
    meta_path = get_metadata_path(model_name)
    with open(meta_path, "w") as f:
        json.dump(data, f, indent=2)

def update_last_used(model_name: str):
    meta = load_metadata(model_name)
    meta["last_used"] = datetime.utcnow().isoformat()
    save_metadata(model_name, meta)
