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
        # self.file_path = self.get_latest_csv_file()

    # @staticmethod
    # def save_json_to_file(data, filename="data.json"):
    #     try:
    #         with open(Path(JSON_FOLDER) / filename, "w", encoding="utf-8") as file:
    #             json.dump(data, file, indent=4, ensure_ascii=False)
    #             print(f"JSON-data lagret i {filename}")
    #     except Exception as e:
    #         print(f"Error while saving JSON file: {e}")

    # @staticmethod
    # def save_any_json_data(data, filename="output", file_format="json"):
    #     try:
    #         if file_format == "json":
    #             FileProcessor.save_json_to_file(data, f"{filename}.json")

    #         elif file_format == "csv":
    #             FileProcessor.save_json_to_csv(data, f"{filename}.csv")

    #         else:
    #             print("Invalid file format.")
    #     except Exception as e:
    #         print(f"Error while saving data: {e}")

    # def get_latest_csv_file(self):
    #     csv_files = list(Path(CSV_FOLDER).glob("*.csv"))
    #     if not csv_files:
    #         print("No CSV files found.")
    #         return None

    #     latest_file = max(csv_files, key=os.path.getmtime)
    #     return latest_file

    # # chose to remove panda because we dont have big data sets
    # def export_as_excel(self):
    #     if self.data is None:
    #         print("No data available to export.")
    #         return
    #     try:
    #         wb = Workbook()
    #         ws = wb.active
    #         ws.append(list(self.data[0].keys()))

    #         for row in self.data:
    #             ws.append(list(row.values()))

    #         output_excel = Path(EXPORTS_FOLDER) / (self.file_path.stem + ".xlsx")
    #         wb.save(output_excel)
    #         print("Csv file exported to excel successfully")

    #     except Exception as e:
    #         print(f"Error occured while exporting file: {e}")

    # def export_data(self, filename, data):
    #     if filename is None:
    #         raise ValueError("Needs a filename")
    #         return

    #     if isinstance(data, dict):
    #         data = [data]
    #     # removes .csv or .json if that is in the filename
    #     filename = filename.rsplit(".", 1)[0]
    #     # save data as csv
    #     try:
    #         csv_filepath = Path(CSV_FOLDER) / f"{filename}.csv"
    #         with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
    #             writer = csv.DictWriter(file, fieldnames=data[0].keys())
    #             writer.writeheader()
    #             writer.writerows(data)

    #         print(f"JSON-data saved in CSV-file: {filename}")

    #         excel_filepath = Path(EXPORTS_FOLDER) / f"{filename}.xlsx"
    #         df = pd.read_csv(csv_filepath)
    #         df.to_excel(excel_filepath, index=False, engine="openpyxl")

    #         print(f"Excel data saved: {excel_filepath}")
    #     except Exception as e:
    #         print(f"Error while saving CSV file: {e}")

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
                metadata_row = {key: "" for key in fieldnames}
                metadata_row["generated_by"] = f"PEATA v{__version__}"
                data.append(metadata_row)

                writer.writerows(data)

            print(f"✅ JSON-data saved to CSV : {filename}")
        except Exception as e:
            print(f"❌ Error while saving CSV file: {e}")

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

    def generate_filename(result_type="video", serial_number=1, extension="csv"):
        today = datetime.datetime.now().strftime("%Y%m%d")
        return f"{result_type}_result_{today}_{serial_number:03d}.{extension}"


# if __name__ == "__main__":
# file_processor = FileProcessor()
# data = file_processor.open_file()

# if data is not None:
#   file_processor.export_as_excel()
#  file_processor.close_file()


# """ Example Usage """
# file_handler = FileHandler()  # Instantiate the class
# data = file_handler.open_file()

# if data is not None:

# """ Export as PDF and Excel"""
# file_handler.export_as_pdf()
# file_handler.export_as_excel()


# """ Close file """
# file_handler.close_file()
