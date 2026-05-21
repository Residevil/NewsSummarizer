import logging
from pathlib import Path
import json
from datetime import datetime, timedelta
import sys
import os
from ..utils import BASE_DIR

CACHE_FILE = BASE_DIR / "backend" / "storage" / "articles.json"
TIMESTAMP_FILE = BASE_DIR / "backend" / "storage" / "last_updated.txt"
BACKUP_DIR = BASE_DIR / "backend" / "storage" / "cache_backups"

logger = logging.getLogger(__name__)

def _ensure_backup_dir():
    try:
        if not BACKUP_DIR.exists():
            BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create backup directory {BACKUP_DIR}: {e}")
        raise

def is_cache_valid():
    if not TIMESTAMP_FILE.exists():
        return False
    try:
        ts_text = TIMESTAMP_FILE.read_text().strip()
        ts = datetime.fromisoformat(ts_text)
    except Exception as e:
        logger.warning(f"Failed to parse cache timestamp file: {e}")
        return False
    return datetime.now() - ts < timedelta(hours=24)

def load_cache():
    if not CACHE_FILE.exists():
        return []
    try:
        text = CACHE_FILE.read_text()
        return json.loads(text)
    except Exception as e:
        logger.error(f"Failed to load cache file {CACHE_FILE}: {e}")
        return []

def save_cache(articles):
    """
    Save articles to cache, backup previous version, and timestamp the update.
    Uses defined CACHE_FILE and TIMESTAMP_FILE Path objects.
    """
    import shutil

    # Backup current cache if it exists
    if CACHE_FILE.exists():
        try:
            _ensure_backup_dir()
        except Exception as e:
            logger.error(f"Aborting save_cache due to backup dir error: {e}")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"articles_{timestamp}.json"
        try:
            shutil.copy2(str(CACHE_FILE), str(backup_file))
        except Exception as e:
            logger.error(f"Error backing up cache file '{CACHE_FILE}' to '{backup_file}': {e}")

        # Remove backups older than 7 days
        try:
            now = datetime.now()
            for bfile in BACKUP_DIR.iterdir():
                if bfile.is_file():
                    try:
                        mtime = datetime.fromtimestamp(bfile.stat().st_mtime)
                        if now - mtime > timedelta(days=7):
                            try:
                                bfile.unlink()
                                logger.info(f"Old backup {bfile} deleted.")
                            except Exception as delete_ex:
                                logger.error(f"Error deleting old backup {bfile}: {delete_ex}")
                    except Exception as stat_ex:
                        logger.error(f"Error stat-ing backup file {bfile}: {stat_ex}")
        except Exception as e:
            logger.error(f"Error during backup cleanup: {e}")

    try:
        CACHE_FILE.write_text(json.dumps(articles, indent=2))
    except Exception as e:
        logger.error(f"Error writing cache file {CACHE_FILE}: {e}")
        return

    try:
        TIMESTAMP_FILE.write_text(datetime.now().isoformat())
    except Exception as e:
        logger.error(f"Error writing timestamp file {TIMESTAMP_FILE}: {e}")

        # INSERT_YOUR_CODE

def clean_cache():
    """
    Deletes all files in the cache backup directory and resets the main cache and timestamp files.
    """
    try:
        # Remove all backup files
        if BACKUP_DIR.exists():
            for bfile in BACKUP_DIR.iterdir():
                if bfile.is_file():
                    try:
                        bfile.unlink()
                        logger.info(f"Backup file {bfile} deleted during cache clean.")
                    except Exception as e:
                        logger.error(f"Failed to delete backup {bfile}: {e}")
    except Exception as e:
        logger.error(f"Error cleaning backup directory: {e}")

    # Remove main cache file
    try:
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
            logger.info(f"Main cache file {CACHE_FILE} deleted during cache clean.")
    except Exception as e:
        logger.error(f"Error deleting main cache file: {e}")

    # Remove timestamp file
    try:
        if TIMESTAMP_FILE.exists():
            TIMESTAMP_FILE.unlink()
            logger.info(f"Timestamp file {TIMESTAMP_FILE} deleted during cache clean.")
    except Exception as e:
        logger.error(f"Error deleting timestamp file: {e}")


def regular_clean_cache(days_old=7):
    """
    Removes backup files older than `days_old` days from the backup directory.
    """
    try:
        if not BACKUP_DIR.exists():
            logger.info("Backup directory does not exist. No cleanup necessary.")
            return

        now = datetime.now()
        for bfile in BACKUP_DIR.iterdir():
            if bfile.is_file():
                try:
                    mtime = datetime.fromtimestamp(bfile.stat().st_mtime)
                    if now - mtime > timedelta(days=days_old):
                        try:
                            bfile.unlink()
                            logger.info(f"Old backup {bfile} deleted by regular_clean_cache.")
                        except Exception as delete_ex:
                            logger.error(f"Error deleting old backup {bfile}: {delete_ex}")
                except Exception as stat_ex:
                    logger.error(f"Error stat-ing backup file {bfile}: {stat_ex}")
    except Exception as e:
        logger.error(f"Error during regular backup cleanup: {e}")
