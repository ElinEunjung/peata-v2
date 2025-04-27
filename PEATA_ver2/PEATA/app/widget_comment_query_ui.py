from PyQt5.QtWidgets import (
QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QCheckBox, QGroupBox, QComboBox, QTabWidget
)
from widget_common_ui_elements import (  create_button, create_horizontal_line, create_scrollable_area, create_result_control_panel, focus_on_query_value, create_result_table, create_query_control_buttons, create_live_query_preview_panel, create_max_results_selector
)
from api import TikTokApi
from widget_progress_bar import ProgressBar
from widget_data_viewer import PandasModel
from FileProcessor import FileProcessor
from queryFormatter import preferred_order_comment
from api import TikTokApi
import json
import pandas as pd


class CommentQueryUI(QWidget):
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("Comment Query")
        self.api = api
        
        # Variables for pagination
        self.cursor = 0
        self.search_id = None
        self.has_more = False
        self.loaded_data = []
        
        self.init_ui()
        
    def init_ui(self):
        self.tabs = QTabWidget()
        self.simple_tab = self.create_simple_tab()
        self.tabs.addTab(self.simple_tab, "Simple")
        
        """Comment out for future expansion ( advanced mode)"""
        # self.advanced_tab = self.create_advanced_tab()
        # self.tabs.addTab(self.advanced_tab, "Advanced")
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        
        
    def create_simple_tab(self):
        tab = QWidget()
        layout = QHBoxLayout()
        
        self.simple_query_group = self.create_simple_query_group()
        self.simple_result_group = self.create_result_group_ui(mode="simple")
        self.simple_result_group.setVisible(False) # Hide at first
        
        
        layout.addWidget(self.simple_query_group)
        layout.addWidget(self.simple_result_group)

        tab.setLayout(layout)
        return tab
       
    def create_simple_query_group(self):    
        # Query Input UI : Query Group(Video ID input + Max result +  Preview)
        container = QWidget()
        main_layout = QHBoxLayout() 
        
        # Left : Video ID input + Help label + Max result selection
        
        self.live_preview_group, self.query_preview = create_live_query_preview_panel()
        self.query_preview = self.live_preview_group.findChild(QTextEdit)
        
        main_layout.addLayout(self.create_simple_left_query_panel(), 3)
        main_layout.addWidget(self.live_preview_group, 2)  
        
        container.setLayout(main_layout) 
        
        self.update_query_preview() # Show default query
        return container
    
    def create_simple_left_query_panel(self):
        layout = QVBoxLayout()
        
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
        # line = create_horizontal_line()
        
        # Max limit selector
        self.max_result_group, self.max_results_selector, self.over_limit_warning_checkbox = create_max_results_selector()
        
        # Buttons
        btn_layout = create_query_control_buttons(self.run_simple_query, self.clear_query)
        
        layout.addWidget(QLabel("Video ID:"))
        layout.addWidget(self.video_id_input)
        layout.addWidget(help_label)
        # layout.addWidget(line)
        layout.addWidget(self.max_result_group)
        layout.addWidget(self.over_limit_warning_checkbox)
        layout.addLayout(btn_layout)
        
        return layout
    
    def create_result_group_ui(self, mode="simple"):
        """Creates the query input section (shared by simple/advanced)."""
        container = QGroupBox("\U0001F4CA Results")
        layout = QHBoxLayout()

        self.table = create_result_table()

        panel = create_result_control_panel(
            on_load_more=self.load_more,
            on_download_csv=self.download_csv,
            on_download_excel=self.download_excel,
            on_back_to_query=self.restore_simple_query_layout
        ) 
        
       
        self.load_more_button = panel["load_more_button"]
        self.download_csv_button = panel["download_csv_button"]
        self.download_excel_button = panel["download_excel_button"]
        self.back_button = panel["back_button"]
        self.load_status_label = panel["load_status_label"]
        self.total_loaded_label = panel["total_loaded_label"]
        

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        self.result_group_layout = panel["group"]

        layout.addLayout(table_layout, 4)
        layout.addWidget(self.result_group_layout, 1)
        container.setLayout(layout)
        return container    
    
    def update_query_preview(self):
        preview_data = self.build_preview_query()
        if self.query_preview:
            self.query_preview.setPlainText(json.dumps(preview_data, indent=4))
        
        # focus_on_query_value(self.query_preview, )
        
    def check_max_limit(self):
        val = self.max_results_selector.currentText()
        if self.over_limit_warning_checkbox.isChecked():
            if val == "ALL" or (val.isdigit() and int(val) == 1000):
                QMessageBox.warning(self, "Warning", "You are requesting a large number of results. This may hit rate limits.")

        
    def run_simple_query(self):
        video_id = self.video_id_input.text().strip()
        if not video_id:
            QMessageBox.warning(self, "Input Error", "Please enter a valid Video ID.")
            return
        
        
        self.video_id = video_id
        self.cursor = 0
        self.loaded_data = []
        
        self.check_max_limit()
        
        selected_text = self.max_results_selector.currentText()
        limit = None if selected_text == "ALL" else int(selected_text)
        
        def fetch():
            return self.api.fetch_comments_basic(video_id, cursor=self.cursor, limit=100)

        def after_fetch(result):
            comments, has_more, cursor, error_msg = result
            
            if error_msg:
                QMessageBox.critical(self, "TikTok API Error", error_msg)
                return
        
            self.loaded_data.extend(comments)
            self.cursor = cursor
            self.has_more = has_more
            
            # If the first page is empty and has more
            if len(self.loaded_data) == 0 and self.has_more:
                print("⚠️ First page empty, trying next page...")   
               
                self.load_more()
                return
            
            self.update_table()
            self.show_simple_result_layout()

           
        ProgressBar.run_with_progress(self, fetch, after_fetch)
        
    
    def show_simple_result_layout(self):
        self.simple_query_group.setVisible(False)
        self.simple_result_group.setVisible(True)
        
    def restore_simple_query_layout(self):
        self.simple_result_group.setVisible(False)
        self.simple_query_group.setVisible(True)
    
    
    
    def update_table(self):
        print(f"[DEBUG] total loaded: {len(self.loaded_data)}, has_more: {self.has_more}")
        df = pd.DataFrame(self.loaded_data)
        
        # Rearrange as "preferred order"
        ordered_columns = [col for col in preferred_order_comment if col in df.columns]
        df = df[ordered_columns + [col for col in df.columns if col not in ordered_columns]]
        
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
            return self.api.fetch_comments_basic(video_id=self.video_id, cursor=self.cursor, limit=100)

        def after_fetch(result):            
            comments, has_more, cursor, error_msg = result
            if error_msg:
                QMessageBox.critical(self, "TikTok API Error", error_msg)
                return
            
            print(f"[DEBUG] API returned:\, {result}")           
            print(f"[DEBUG] comments={len(comments)}, has_more={has_more}, cursor={cursor}")
            
            self.loaded_data.extend(comments)
            self.cursor = cursor
            self.has_more = has_more
            self.update_table()
            self.load_more_button.setVisible(has_more)

        ProgressBar.run_with_progress(self, fetch, after_fetch)
    
    def run_download_with_progress(self, file_format="csv"):
        selected_text = self.max_results_selector.currentText()
        limit = None if selected_text == "ALL" else int(selected_text)

        def task():
            all_data = self.loaded_data[:]
            has_more = self.has_more
            cursor = self.cursor
            while has_more and (limit is None or len(all_data) < limit):
                comments, has_more, cursor, _ = self.api.fetch_comments_basic(
                    video_id=self.video_id,
                    cursor=cursor
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
        self.max_results_selector.setCurrentText("500")
        self.update_query_preview()
        
    # For live preview
    def build_preview_query(self):
        video_id =  self.video_id_input.text().strip() or "example_video_id"
        val = self.max_results_selector.currentText()
        limit = 999999 if val == "ALL" else int(val)
        fields = [           
            "text",
            "like_count",
            "reply_count",
            "create_time",
            "id",
            "parent_comment_id",
            "video_id"
        ]

        return {
            "query": {
                "and": [
                    {
                        "operation": "EQ",
                        "field_name": "video_id",
                        "field_values": [video_id]
                    }
                ]
            },
            "limit": limit,
            "fields": fields
        }
            
    
                
# # For testing
# if __name__ == "__main__":
#     import sys
#     from PyQt5.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     window = CommentQueryUI()
#     window.show()
#     sys.exit(app.exec())
