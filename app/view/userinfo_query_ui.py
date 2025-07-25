"""
Implements the User Info Query panel, including query preview and result display.

Author: Elin
Created: 2025-06-28
Version: v2.0.0
"""

import json

import pandas as pd
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QVBoxLayout, QWidget

from app.controller.query_formatter import preferred_order_userinfo
from app.model.file_processor import FileProcessor

from .common_ui_elements import (
    create_live_query_preview_panel,
    create_query_control_buttons,
    create_result_control_panel,
    create_result_table,
)
from .data_viewer import PandasModel
from .progress_bar import ProgressBar


class UserInfoQueryUI(QWidget):
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("User Info Query")
        self.api = api
        self.result_data = None

        self.init_ui()
        self.update_preview()  # Show default preview on load

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left panel (1)
        left_panel = QVBoxLayout()
        self.label = QLabel("Enter Username:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., lizzo, jxdn, tai_verdes, mxmtoon, chrisudalla")
        self.input_field.textChanged.connect(self.update_preview)

        # Live Query Preview
        preview_panel = create_live_query_preview_panel()  # QGroupBox, text_edit
        self.live_preview_group = preview_panel["group"]
        self.query_preview = preview_panel["text_edit"]

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addLayout(create_query_control_buttons(self.run_query, self.clear_all))

        left_panel.addWidget(self.label)
        left_panel.addWidget(self.input_field)
        left_panel.addLayout(btn_layout)
        left_panel.addWidget(self.live_preview_group)

        # Right panel (3)
        right_outer_panel = QHBoxLayout()

        # Table inside a GroupBox
        table_group = QGroupBox("📊 Results ")
        table_layout = QVBoxLayout()
        self.table = create_result_table()
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        # Result Control Panel
        panel = create_result_control_panel(
            on_load_more=lambda: None,  # No use Load more button
            on_download_csv=self.download_csv,
            on_download_excel=self.download_excel,
            on_back_to_query=lambda: None,
        )

        self.download_csv_button = panel["download_csv_button"]
        self.download_excel_button = panel["download_excel_button"]
        self.load_status_label = panel["load_status_label"]

        self.result_group_layout = panel["group"]
        self.back_button = panel["back_button"]
        self.back_button.setVisible(False)

        # Right inner layout : table 3: control panel 1
        right_outer_panel.addWidget(table_group, 3)
        right_outer_panel.addWidget(self.result_group_layout, 1)

        # Merge Left and Right
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_outer_panel, 3)

        self.setLayout(main_layout)

    def update_preview(self):
        username = self.input_field.text().strip() or "example_user_id"

        preview = {
            "query": {
                "and": [
                    {
                        "operation": "EQ",
                        "field_name": "username",
                        "field_values": [username],
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
                "video_count",
            ],
        }
        self.query_preview.setPlainText(json.dumps(preview, indent=2))
        # focus_on_query_value(self.preview_box, username)

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

            info["username"] = username  # Save Search Term
            self.result_data = [info]

            # Set preordered column
            df = pd.DataFrame(self.result_data)
            ordered_cols = [col for col in preferred_order_userinfo if col in df.columns]
            remaining_cols = [col for col in df.columns if col not in ordered_cols]
            df = df[ordered_cols + remaining_cols]

            self.table.setModel(PandasModel(df))

        ProgressBar.run_with_progress(self, fetch_user, after_fetch)

    def download_csv(self, file_format="csv"):
        if not self.result_data:
            QMessageBox.warning(self, "No Data", "Please run a query first.")
            return

        filename = FileProcessor.generate_filename(result_type="userinfo", serial_number=1, extension="csv")
        FileProcessor().export_with_preferred_order(self.result_data, filename, "csv")

        QMessageBox.information(self, "Saved", "CSV file saved successfully.")

    def download_excel(self, file_format="xlsx"):
        if not self.result_data:
            QMessageBox.warning(self, "No Data", "Please run a query first.")
            return

        filename = FileProcessor.generate_filename(result_type="userinfo", serial_number=1, extension="xlsx")
        FileProcessor.export_with_preferred_order(self.result_data, filename, "xlsx")
        QMessageBox.information(self, "Saved", "Excel file saved successfully.")

    def clear_all(self):
        self.input_field.clear()
        self.query_preview.clear()
        self.result_data = None
        self.table.setModel(None)
