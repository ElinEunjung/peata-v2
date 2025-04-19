from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from api import TikTokApi
from widget_common_ui_elements import focus_on_query_value, create_button, create_result_table, create_result_control_panel
from FileProcessor import FileProcessor
from widget_data_viewer import PandasModel
from widget_progress_bar import ProgressBar
from error_utils import get_friendly_error_message
import pandas as pd
import json



"""
Todo:

- Check (username) value before excute run_query()
- Consider better file name

UserInfo Query Ui work flow   
- Input : Username
- Call Api : get_public_user_info(username) + Progress bar
- Treat result: Print result with JSON on text view
"""

class UserInfoQueryUI(QWidget):
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("User Info Query")
        self.api = api 
        self.result_data = None
        
        self.init_ui()
        self.update_preview() # Show default preview on load

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left panel
        left_panel = QVBoxLayout()
        self.label = QLabel("Enter Username:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(
            "Enter a TikTok username: e.g., lizzo, jxdn, tai_verdes, mxmtoon, chrisudalla, kingxsosa, itsjojosiwa"
)
        self.input_field.textChanged.connect(self.update_preview)

        
        # Live Query Preview
        self.preview_box = QTextEdit()
        self.preview_box.setReadOnly(True)
        self.preview_box.setMinimumHeight(150)
        
        # Buttons
        self.run_button = create_button("Run Query", click_callback=self.run_query)
        self.clear_button = create_button("Clear Query", click_callback=self.clear_all)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.run_button)
        btn_layout.addWidget(self.clear_button)
        
        left_panel.addWidget(self.label)
        left_panel.addWidget(self.input_field)
        left_panel.addWidget(QLabel("Live Query Preview:"))
        left_panel.addWidget(self.preview_box)
        left_panel.addLayout(btn_layout)
        
        # Right panel (Table + Control Panel)
        right_panel = QHBoxLayout()
        
        self.result_table = create_result_table()
        self.result_panel, _, _, _ = create_result_control_panel(
            on_load_more=lambda: None, # No use Load more button
            on_download_csv=self.download_csv,
            on_download_excel=self.download_excel
        )
        
        
        right_panel.addWidget(self.result_table)
        right_panel.addWidget(self.result_panel)
        
        # Merge Layouts
        main_layout.addLayout(left_panel, 2)
        main_layout.addLayout(right_panel, 3)
        self.setLayout(main_layout)


    def update_preview(self):
        username = self.input_field.text().strip() or "example_user_id"
       
        preview = {
            "query": {
                "and": [
                    {
                        "operation": "EQ",
                        "field_name": "username",
                        "field_values": [username]
                    }
                ]
            },
            "fields": [
                "display_name",
                "bio_description",
                "avatar_url",
                "is_verified",
                "follower_count",
                "following_count",
                "likes_count",
                "video_count"
            ]
        }
        self.preview_box.setPlainText(json.dumps(preview, indent=2))
        focus_on_query_value(self.preview_box, username)
        
    def run_query(self):
        username = self.input_field.text().strip()
        if not username:
            QMessageBox.warning(self, "Input Error", "Please enter a username.")
            return
        
        def fetch_user():
            return self.api.get_public_user_info(username)
        
        
        def after_fetch(info):
            if not info:
                QMessageBox.information(self, "No Results", "No user found.")
                return
    
            self.result_data = [info]
            df = pd.DataFrame(self.result_data)
            self.result_table.setModel(PandasModel(df))
            
        ProgressBar.run_with_progress(self, fetch_user, after_fetch)
    
    def download_csv(self):
        if not self.result_data:
            QMessageBox.warning(self, "No Data", "Please run a query first.")
            return
        FileProcessor.export_with_preferred_order(self.result_data, "user_info_result", "csv")
        QMessageBox.information(self, "Saved", "CSV file saved successfully.")

    def download_excel(self):
        if not self.result_data:
            QMessageBox.warning(self, "No Data", "Please run a query first.")
            return
        FileProcessor.export_with_preferred_order(self.result_data, "user_info_result", "excel")
        QMessageBox.information(self, "Saved", "Excel file saved successfully.")
        
    def clear_all(self):
       self.input_field.clear()
       self.preview_box.clear()
       self.result_box.setPlainText("Result will show here") 
    
       
# # For testing
# if __name__ == "__main__":
#     import sys
#     from PyQt5.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     window = UserInfoQueryUI()
#     window.show()
#     sys.exit(app.exec())