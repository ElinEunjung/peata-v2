"""
Handles saving query results to CSV or Excel files
by exporting with preferred column orders and including auto-generated metadata.

Original Author: PEATA Team (Elin & Oda)
Refactored & documented by : Elin
Date: 2025-06-28
Version: v2.0.0
"""

import csv
import datetime
import json
from pathlib import Path

import pandas as pd

from app import __version__
from app.controller.query_formatter import preferred_order_comment, preferred_order_userinfo, preferred_order_video

from .config import CSV_FOLDER, EXCEL_FOLDER


class FileProcessor:

    def __init__(self):
        self.data = None

    # Added function for Gui ver.2
    @staticmethod
    def export_with_preferred_order(data, filename, file_format="csv"):

        if "video" in filename.lower():
            field_order = preferred_order_video
        elif "comment" in filename.lower():
            field_order = preferred_order_comment
        elif "user" in filename.lower():
            field_order = preferred_order_userinfo
        else:
            field_order = None

        # Add file extention automatically
        if file_format == "excel" and not filename.endswith(".xlsx"):
            filename += ".xlsx"
        elif file_format == "csv" and not filename.endswith(".csv"):
            filename += ".csv"

        # Excute Save
        if file_format == "excel":
            FileProcessor.save_json_to_excel(data, filename, field_order)
        else:
            FileProcessor.save_json_to_csv(data, filename, field_order)

    # Added function for Gui ver.2
    @staticmethod
    def save_json_to_excel(data, filename="data.xlsx", field_order=None):

        if not data:
            print("No data to save.")
            return

        if field_order:
            df = pd.DataFrame(data).reindex(columns=field_order)
        else:
            df = pd.DataFrame(data)

        filepath = Path(EXCEL_FOLDER) / filename
        df.to_excel(filepath, index=False)
        print(f"✅ Data saved to Excel: {filename}")

    # Added function for Gui ver.2
    @staticmethod
    def generate_filename(result_type="video", serial_number=1, extension="csv"):
        today = datetime.datetime.now().strftime("%Y%m%d")
        return f"{result_type}_result_{today}_{serial_number:03d}.{extension}"

    # function from ver.1
    @staticmethod
    def save_json_to_csv(data, filename="data.csv", field_order=None):
        if not data or not isinstance(data, list) or not isinstance(data[0], dict):
            print("No valid data to save")
            return

        try:
            filepath = Path(CSV_FOLDER) / filename

            # Define fieldsname by Preferred order
            if field_order:
                fieldnames = field_order
            else:
                fieldnames = set()
                for row in data:
                    fieldnames.update(row.keys())
                fieldnames = list(fieldnames)

            # Convert list/dic to JSON string
            for row in data:
                for key, value in row.items():
                    if isinstance(value, (list, dict)):
                        row[key] = json.dumps(value, ensure_ascii=False)

            # Save as CSV
            with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                # Add metadata row
                data_to_write = data.copy()
                metadata_row = {key: "" for key in fieldnames}
                metadata_row["generated_by"] = f"PEATA v{__version__}"
                data_to_write.append(metadata_row)
                writer.writerows(data_to_write)

        except Exception as e:
            print(f"❌ Error while saving CSV file: {e}")
