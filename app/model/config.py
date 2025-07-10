"""
Sets up base paths and ensures existence of folders for data exports (CSV and Excel).

Author: Elin
Created: 2025-06-28
Version: v2.0.0
"""

import sys
from pathlib import Path


def get_base_dir():
    """
    Returns the correct base path for saving files.
    If running from .exe, use the directory of the executable.
    If running from source, use the project root.
    """
    if getattr(sys, "frozen", False):
        # Running from PyInstaller bundle
        return Path(sys._MEIPASS).parent
    else:
        # Running from source (normal)
        # Base directory (peata-v2) is three levels up (peata-v2/app/model/config.py)
        return Path(__file__).resolve().parent.parent.parent


BASE_DIR = get_base_dir()


# Export folders (outside the .exe)
CSV_FOLDER = BASE_DIR / "data" / "csv"
EXCEL_FOLDER = BASE_DIR / "data" / "excel"

# Ensure folders exist
CSV_FOLDER.mkdir(parents=True, exist_ok=True)
EXCEL_FOLDER.mkdir(parents=True, exist_ok=True)
