import os

BASE_FOLDER = "data"
CSV_FOLDER = os.path.join(BASE_FOLDER, "csv")
EXCEL_FOLDER = os.path.join(BASE_FOLDER, "excel")

# Ensure folders exist
os.makedirs(CSV_FOLDER, exist_ok=True)
os.makedirs(EXCEL_FOLDER, exist_ok=True)
