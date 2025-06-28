"""
Sets up base paths and ensures existence of folders for data exports (CSV and Excel).

Author: Elin
Created: 2025-06-28
Version: v2.0.0
"""

from pathlib import Path

# Base directory is two levels up (project root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Export folders
CSV_FOLDER = BASE_DIR / "data" / "csv"
EXCEL_FOLDER = BASE_DIR / "data" / "excel"

# Ensure folders exist
CSV_FOLDER.mkdir(parents=True, exist_ok=True)
EXCEL_FOLDER.mkdir(parents=True, exist_ok=True)
