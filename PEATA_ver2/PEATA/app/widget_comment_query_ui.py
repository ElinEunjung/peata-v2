from PyQt5.QtWidgets import (
QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QCheckBox, QGroupBox, QComboBox, QTabWidget
)
from widget_common_ui_elements import (  create_button, create_horizontal_line, create_scrollable_area, create_result_control_panel, focus_on_query_value, create_result_table
)
from api import TikTokApi
from widget_progress_bar import ProgressBar
from widget_data_viewer import PandasModel
from FileProcessor import FileProcessor
from api import TikTokApi
import json
import pandas as pd


class CommentQueryUI(QWidget):
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("Comment Query")
        self.api = api
        self.query_body = {}
        self.cursor = 0
        self.search_id = None
        self.has_more = False
        self.loaded_data = []
        
        self.init_ui()
        
    def init_ui(self):
        self.tabs = QTabWidget()
        self.simple_tab = self.create_simple_tab()
        self.tabs.addTab(self.simple_tab, "Simple")
        
        """
        Future expansion for advanced mode!
        """
        # self.advanced_tab = self.create_advanced_tab()
        # self.tabs.addTab(self.advanced_tab, "Advanced")
        
        self.query_group = QWidget()
        query_layout = QVBoxLayout()
        query_layout.addWidget(self.tabs)
        self.query_group.setLayout(query_layout)

        self.result_group = self.create_result_panel()
        self.result_group.setVisible(False)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.query_group)
        main_layout.addWidget(self.result_group)
        self.setLayout(main_layout)
        
        
    def create_simple_tab(self):
        tab = QWidget()
        layout = QHBoxLayout()
        
        # Left Panel
        left_panel = QVBoxLayout()
        self.video_id_input = QLineEdit()
        self.video_id_input.setPlaceholderText("Enter TikTok Video ID (e.g., 702874395068494965)")
        self.video_id_input.textChanged.connect(self.update_query_preview)
        
        # User hint text (style added in style.qss)
        help_label = QLabel(
        "Example URL: https://www.tiktok.com/@username/video/702874395068494965\n"
        "→ Copy only the last number as Video ID: 702874395068494965"
        )
        help_label.setWordWrap(True)
        help_label.setObjectName("HelperLabel")
        
        # Add <hr>
        line = create_horizontal_line()
        
        # Max Results Selector
        self.max_results_selector = QComboBox()
        self.max_results_selector.addItems(["100", "500", "1000", "ALL"])
        self.max_results_selector.setCurrentText("500")
        self.max_results_selector.currentTextChanged.connect(self.check_max_limit)

        self.over_limit_warning_checkbox = QCheckBox("Warn if result count exceeds 1000")
        self.over_limit_warning_checkbox.setChecked(True)
        self.over_limit_warning_checkbox.setToolTip("Disable this if you want to skip warnings for large requests (over 1000 results).")

        # Buttons
        self.run_button = create_button("Run Query", click_callback=self.run_query)
        self.clear_button = create_button("Clear Query", click_callback=self.clear_query)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.run_button)
        btn_layout.addWidget(self.clear_button)
        
        left_panel.addWidget(QLabel("Video ID:"))
        left_panel.addWidget(self.video_id_input)
        left_panel.addWidget(help_label)
        left_panel.addWidget(line)
        left_panel.addWidget(QLabel("Max Results:"))
        left_panel.addWidget(self.max_results_selector)
        left_panel.addWidget(self.over_limit_warning_checkbox)
        left_panel.addLayout(btn_layout)
       
        # Right Panel - Live Query Preview
        right_panel = QVBoxLayout()
        self.query_preview = QTextEdit()
        self.query_preview.setReadOnly(True)
        self.query_preview.setMinimumHeight(200)
        scrollable_preview = create_scrollable_area(self.query_preview)

        preview_layout = QVBoxLayout()
        preview_layout.addWidget(QLabel("Live Query Preview"))
        preview_layout.addWidget(scrollable_preview)
        
        self.preview_group = QGroupBox("\U0001F9E0 Live Query Preview")
        self.preview_group.setLayout(preview_layout)

        right_panel.addWidget(self.preview_group)

        layout.addLayout(left_panel, 2)
        layout.addLayout(right_panel, 3)
        tab.setLayout(layout)
        
        self.update_query_preview()  # Show default preview on load
        
        return tab
    
    def create_advanced_tab(self):
        # Future expansion for advanced mode
        pass
    
    def create_result_panel(self):
        container = QGroupBox("\U0001F4CA Results")
        layout = QHBoxLayout()

        self.table = create_result_table()
        self.total_loaded_label = QLabel("No data loaded.")
        self.load_status_label = QLabel("")

        self.result_control_panel,          self.load_more_button, load_status, total_loaded, self.back_button = create_result_control_panel(
            on_load_more=self.load_more,
            on_download_csv=self.download_csv,
            on_download_excel=self.download_excel,
            on_back_to_query=self.restore_query_layout
        )

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)

        layout.addLayout(table_layout, 4)
        layout.addWidget(self.result_control_panel, 1)
        container.setLayout(layout)
        return container    
    
    def update_query_preview(self):
        video_id = self.video_id_input.text().strip() or "example_video_id"
          
        # self.query_body = preview
        preview = {
            "query": {
                "and": [
                    {
                        "operation": "EQ",
                        "field_name": "video_id",
                        "field_values": [video_id]
                    }
                ]
            }
        }
        self.query_preview.setPlainText(json.dumps(preview, indent=2))
        focus_on_query_value(self.query_preview, video_id)
        
    def check_max_limit(self):
        val = self.max_results_selector.currentText()
        if val != "ALL" and int(val) > 1000 and self.over_limit_warning_checkbox.isChecked():
            QMessageBox.warning(self, "Warning", "You are requesting more than 1000 results. This may hit rate limits.")
        
    def run_query(self):
        video_id = self.video_id_input.text().strip()
        if not video_id:
            QMessageBox.warning(self, "Input Error", "Please enter a valid Video ID.")
            return

        self.cursor = 0
        self.loaded_data = []

        def fetch():
            return self.api.get_comments_by_page(video_id, cursor=self.cursor)

        def after_fetch(result):
            comments, has_more, cursor, _ = result
            self.loaded_data.extend(comments)
            self.cursor = cursor
            self.has_more = has_more
            self.update_table()
            self.show_result_layout()

        ProgressBar.run_with_progress(self, fetch, after_fetch)

    def restore_query_layout(self):
        self.result_group.setVisible(False)
        self.query_group.setVisible(True)
    
    def show_result_layout(self):
        self.query_group.setVisible(False)
        self.result_group.setVisible(True)
    
    def update_table(self):
        print(f"[DEBUG] total loaded: {len(self.loaded_data)}, has_more: {self.has_more}")
        df = pd.DataFrame(self.loaded_data)
        model = PandasModel(df)
        self.table.setModel(model)
        self.total_loaded_label.setText(f"{len(self.loaded_data)} comments loaded.")
        self.update_load_status()
        self.load_more_button.setVisible(self.has_more)
    
    def update_load_status(self):
        current = len(self.loaded_data)
        selected_text = self.max_results_selector.currentText()
        max_limit = "∞" if selected_text == "ALL" else selected_text
        self.load_status_label.setText(f"Loaded {current} / {max_limit}")
    
    def load_more(self):
        def fetch():
            return self.api.get_comments_by_page(self.query_body["video_id"], cursor=self.cursor)

        def after_fetch(result):            
            comments, has_more, cursor, error_message = result
            if error_message:
                QMessageBox.critical(self, "TikTok API Error", error_message)
                return
            
            print(f"[DEBUG] API returned:\, {result}")           
            print(f"[DEBUG] comments={len(comments)}, has_more={has_more}, cursor={cursor}")
            
            self.loaded_data.extend(comments)
            self.cursor = cursor
            self.has_more = has_more
            self.update_table()
            self.show_result_layout()

        ProgressBar.run_with_progress(self, fetch, after_fetch)
    
    def run_download_with_progress(self, file_format="csv"):
        selected_text = self.max_results_selector.currentText()
        limit = None if selected_text == "ALL" else int(selected_text)

        def task():
            all_data = self.loaded_data[:]
            has_more = self.has_more
            cursor = self.cursor
            while has_more and (limit is None or len(all_data) < limit):
                comments, has_more, cursor, _ = self.api.get_comments_by_page(
                    self.query_body["video_id"], cursor=cursor
                )
                all_data.extend(comments)
            return all_data[:limit] if limit else all_data

        def on_done(data):
            if not data:
                QMessageBox.information(self, "No Data", "No data available to download.")
                return
            FileProcessor.export_with_preferred_order(data, "comments_result", file_format)
            QMessageBox.information(self, "Download Complete", f"Your {file_format} file with {len(data)} items saved successfully.")

        ProgressBar.run_with_progress(self, task, on_done)
        
    def download_csv(self):
        self.run_download_with_progress("csv")

    def download_excel(self):
        self.run_download_with_progress("excel")

    def clear_query(self):
        self.video_id_input.clear()
        self.query_preview.clear()
        self.loaded_data.clear()
        self.cursor = 0
        self.search_id = None
        self.has_more = False
        self.table.setModel(None)
        self.total_loaded_label.setText("No data loaded.")
        self.load_status_label.setText("")
        
# # For testing
# if __name__ == "__main__":
#     import sys
#     from PyQt5.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     window = CommentQueryUI()
#     window.show()
#     sys.exit(app.exec())
