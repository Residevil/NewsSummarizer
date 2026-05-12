import sys
from pathlib import Path

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

BASE_DIR = get_base_dir()
TEMPLATE_PATH = BASE_DIR / "backend" / "templates" / "digest.html"