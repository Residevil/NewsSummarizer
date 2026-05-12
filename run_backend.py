import uvicorn
from backend.main import app
from backend.utils import get_base_dir
import logging
import os

def main():
    base = get_base_dir()
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Backend starting with BASE_DIR = {base}")

    # Ensure storage directories exist
    storage_dir = base / "backend" / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=39231,
        log_level="info"
    )

if __name__ == "__main__":
    main()
