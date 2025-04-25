# from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QComboBox, QTabWidget, QMessageBox, QCheckBox, QGroupBox, QLayout, QDateEdit
    )
from widget_common_ui_elements import (
    create_date_range_widget, create_result_table,
    create_collapsible_section, create_labeled_input,
    create_checkbox_with_tooltip, create_button,
    create_field_group_with_emojis, 
create_horizontal_line, focus_on_query_value,
    create_multi_select_input,
    create_result_control_panel,
    create_query_control_buttons, create_live_query_preview_panel,
    create_max_results_selector,
    )
from widget_region_codes import REGION_CODES, get_flag_emoji
from widget_progress_bar import ProgressBar
from api import TikTokApi
from queryFormatter import QueryFormatter
from FileProcessor import FileProcessor
from widget_data_viewer import PandasModel
import json


class VideoQueryUI(QWidget):
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("Video Query Builder")
        self.region_codes = REGION_CODES
        
        self.api = api
        
        self.logic_ops = {
            "AND (All must match)": "and",
            "OR (Any can match)": "or",
            "NOT (Exclude)": "not"
        }
                
        self.condition_ops = {           
            "Equals": "EQ",
            "IN": "IN",
            "Greater than": "GT",
            "Greater or equal": "GTE",
            "Less than": "LT",
            "Less or equal": "LTE"
        }
        
        self.filterable_fields = [
            "video_id",
            "username",
            "keyword",
            "region_code",
            "hashtag_name",
            "music_id",
            "effect_ids",
            "video_length",
            "create_time"
        ]

        self.supported_operators = {
            "video_id": ["EQ", "IN"],
            "username": ["EQ", "IN"],
            "keyword": ["EQ", "IN"],
            "region_code": ["EQ", "IN"],
            "hashtag_name": ["EQ", "IN"],
            "music_id": ["EQ", "IN"],
            "effect_ids": ["EQ", "IN"],
            "video_length": ["EQ", "IN"],
            "create_time": ["EQ", "IN", "GT", "GTE", "LT", "LTE"],        
        }
       
        self.placeholder_map = {
            "username" : "e.g., cookie_lover_elin",
            "keyword" : "e.g., arianagrande, celebrity",
            "hashtag_name" : "e.g., tiktok, coffee",
            "music_id" : "8978345345214861235",
            "effect_ids" : "3957392342148643476",
            "video_id" : "6978662169214864645"
            }
            # "region_code", "video_length" will be replaced with dropdown menu
            # "create_time" will use QDateEdit

        self.default_operators = {
            "video_id": "EQ",
            "username": "IN",
            "keyword": "IN",
            "region_code": "IN",
            "hashtag_name": "IN",
            "music_id": "IN",
            "effect_ids": "IN",
            "video_length": "EQ",
            "create_time": "GTE"  # Eventually selectable in UI
}
        
        self.all_supported_fields = []
        for group in [CREATOR_FIELDS, POSTING_FIELDS, ENGAGEMENT_FIELDS, TAGS_FIELDS, ADVANCED_FIELDS]:
            self.all_supported_fields.extend(group.keys())
        
        # Variables for pagination
        self.current_query = None
        self.cursor = 0
        self.search_id = None
        self.has_more = False
        self.loaded_data = []
        
        # Variable for filter condition 
        self.logic_filter_rows = {}
        self.init_ui()
        self.connect_live_query_signals()
    
    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_advanced_tab(), "Advanced")
        
        """Future expansion for simple mode! """
        # self.tabs.addTab(self.create_simple_tab(), "Simple")
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        
    
    def connect_live_query_signals(self):
        # Date range → update + highlight
        self.start_date.dateChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.start_date.date().toString("yyyyMMdd"))
        ))
        self.end_date.dateChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.end_date.date().toString("yyyyMMdd"))
        ))
        
        # All field checkboxes → update only
        for checkbox in self.field_checkboxes.values():
            checkbox.stateChanged.connect(self.update_query_preview)
 
            
    def _connect_highlighted_input(self, widget, extract_fn):
        widget.textChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview,extract_fn(widget))
        )) 
        
    def _connect_field_change(self, row: QHBoxLayout):
          print("🛠️ Connecting signals for row...")
          
          if row.count() < 3:
              print("⚠️ Skipping row: not enough widgets.")
              return
          
          # Extract widgets from the filter row
          field_selector = row.itemAt(0).widget()
          op_selector = row.itemAt(1).widget()
          value_container = row.itemAt(2).widget()
          value_container_layout = value_container.layout() 
      
          # Connnect field selector (QComboBox) changes
                
          if isinstance(field_selector, QComboBox):
              field_selector.currentTextChanged.connect(self.update_query_preview)
      
          # Connect operator selector (QComboBox) changes
          if isinstance(op_selector, QComboBox):
              op_selector.currentTextChanged.connect(self.update_query_preview)
      
          # Connect value input widget changes
          if value_container_layout and value_container_layout.count() > 0:
              value_widget = value_container_layout.itemAt(0).widget()
              
              if isinstance(value_widget, QLineEdit):
                value_widget.textChanged.connect(lambda: (
                    self.update_query_preview(),
                    focus_on_query_value(self.query_preview, value_widget.text())
                ))
              elif isinstance(value_widget, QComboBox):
                    value_widget.currentTextChanged.connect(lambda: (
                        self.update_query_preview(),
                        focus_on_query_value(self.query_preview, value_widget.currentText())
                    ))
              elif isinstance(value_widget, QDateEdit):
                    value_widget.dateChanged.connect(lambda: (
                        self.update_query_preview(),
                        focus_on_query_value(self.query_preview, value_widget.date().toString("yyyyMMdd"))
                    ))

    
    def update_query_preview(self):
        query = self.build_query()
        
        preview = self.query_preview
        if preview :
            preview.setPlainText(json.dumps(query, indent=2))
        
    def create_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
    
        self.advanced_query_group = self.create_advanced_query_group_ui()
        self.advanced_result_group = self.create_result_group_ui()
        self.advanced_result_group.setVisible(False) # Hide at first
    
        layout.addWidget(self.advanced_query_group)
        layout.addWidget(self.advanced_result_group)
    
        tab.setLayout(layout)
        return tab
    
    def create_advanced_query_group_ui(self):
        # Query Input UI : Query Group(Field + Filter + Preview)
        group = QGroupBox("🔎 Advanced Query Builder")
        container = QWidget()
        main_layout = QHBoxLayout()  
    
        # LEFT: Field Selection + Filter Builder Query Control Buttons
        left_panel = QVBoxLayout()
        
        # Top row: Select Field + Fiter Buidler
        top_row_layout = QHBoxLayout()
        top_row_layout.addWidget(self.create_field_selection_panel())
        top_row_layout.addWidget(self.create_filter_builder_panel())        
        left_panel.addLayout(top_row_layout)
        
        # Bottom row: Run/Clear Button
        bottom_row_layout = QHBoxLayout()
#         bottom_row_layout.addLayout(
#     create_query_control_buttons(self.run_advanced_query, self.clear_query)
# )
        left_panel.addLayout(bottom_row_layout) 
        
        # Max Results Selector
        self.max_result_group, self.max_results_selector, self.over_limit_warning_checkbox = create_max_results_selector()
        
        left_panel.addWidget(self.max_result_group)
        
        left_container = QWidget()
        left_container.setLayout(left_panel)
        main_layout.addWidget(left_container, 3)
        
        # RIGHT: Live Query Preview
        preview_panel = create_live_query_preview_panel()  # QGroupBox, text_edit
        self.live_preview_group = preview_panel["group"]
        self.query_preview = preview_panel["text_edit"]
        
        main_layout.addWidget(self.live_preview_group, 2)  
    
        container.setLayout(main_layout) 
        group.setLayout(QVBoxLayout())
        group.layout().addWidget(container)
        
        self.update_query_preview() # Show default query
        self.connect_live_query_signals()
        
        return group
    
    def create_result_group_ui(self):
        group = QGroupBox("📊 Results (Advanced)")
        layout = QVBoxLayout()
        
        self.table = create_result_table()
        layout.addWidget(self.table)
    
        panel = create_result_control_panel(
            on_load_more=self.load_more,
            on_download_csv=self.download_csv,
            on_download_excel=self.download_excel,
            on_back_to_query=self.restore_advanced_query_layout
)

        self.result_control_panel = panel["group"]
        self.load_more_button = panel["load_more_button"]
        self.load_status_label = panel["load_status_label"]
        self.total_loaded_label = panel["total_loaded_label"]
        self.back_button = panel["back_button"]
        
        layout.addWidget(self.result_control_panel)
    
        group.setLayout(layout)
        return group
        
    def create_field_selection_panel(self):
        self.field_checkboxes = {} # Save all fields checked status
        fields_layout = QVBoxLayout()
    
        # Add sub-groups : Creator, Posting, Engagement, Tags
        for title, fields in [
            ("🧑‍💻 Creator Info", CREATOR_FIELDS),
            ("📅 Posting Info", POSTING_FIELDS),
            ("📊 Engagement", ENGAGEMENT_FIELDS),
            ("🏷️ Tags & Metadata", TAGS_FIELDS)
        ]:
            group_widget = create_field_group_with_emojis(
                title, fields, self.field_checkboxes, default_checked=True
            )
            fields_layout.addWidget(group_widget)
    
        # Advanced fileds inside collapsible section + checked status
        advanced_widget = create_field_group_with_emojis(
            "", ADVANCED_FIELDS, self.field_checkboxes, default_checked=True
        )
        collapsible = create_collapsible_section("🧪 Advanced Fields", advanced_widget, checked=True)
        fields_layout.addWidget(collapsible)
        
        # Wrap everything inside a "Fields" group box
        fields_group = QGroupBox("🧾 Fields to include in result")
        fields_group.setLayout(fields_layout)
        
        return fields_group
    
    def create_filter_builder_panel(self):
        container = QWidget()
        main_layout = QVBoxLayout()
        
        # Filter Group Container (Add AND/OR/NOT Group)
        self.filter_group_container = QVBoxLayout()
        self.logic_groups = {}

        # Create/Add AND group (include basic filter)
        and_group = self.create_filter_group_ui("AND", include_base=True)
        self.logic_groups["AND"] = and_group
        self.filter_group_container.addWidget(and_group)
    
    
        # Button layout
        self.add_or_btn = create_button("+ Add OR Group", object_name="logic-group-btn")
        self.add_not_btn = create_button("+ Add NOT Group", object_name="logic-group-btn")
        self.add_or_btn.clicked.connect(lambda: self.add_logic_group("OR"))
        self.add_not_btn.clicked.connect(lambda: self.add_logic_group("NOT"))
        
        
        group_btn_layout = QVBoxLayout()
        group_btn_layout.addWidget(self.add_or_btn)
        group_btn_layout.addWidget(self.add_not_btn)
        #Add to main_layout
        group_container_widget = QWidget()
        group_container_widget.setLayout(self.filter_group_container)
        main_layout.addWidget(group_container_widget)
        main_layout.addLayout(group_btn_layout)

        container.setLayout(main_layout)
        return container

    def add_logic_group(self, logic_type: str):
        # Create Group    
        group = self.create_filter_group_ui(logic_type, include_base=False)
        self.logic_groups[logic_type] = group
        self.filter_group_container.addWidget(group)

        #Disable buttons
        if logic_type == "OR":
            self.add_or_btn.setVisible(False)
            
        elif logic_type == "NOT":
            self.add_not_btn.setVisible(False)
    
    def create_filter_group_ui(self, logic_type: str, include_base: bool = False):
        # Ui for Adding filter to categorized logic operators
        group_box = QGroupBox(f"{logic_type} Filter Group")
        layout = QVBoxLayout()
        
        if logic_type == "AND":
            layout.addLayout(self._create_date_range_row(layout, group_box))
            layout.addLayout(self._create_filter_row(logic_type, layout, group_box, "username"))
            layout.addLayout(self._create_filter_row(logic_type, layout, group_box, "keyword"))
            layout.addLayout(self._create_filter_row(logic_type, layout, group_box, "create_time"))
            layout.addLayout(self._create_filter_row(logic_type, layout, group_box, "region_code"))
        else:
            layout.addLayout(self._create_filter_row(logic_type, layout, group_box))
                       
        # Fixed button at the bottom
        add_btn = create_button(f"+ Add Filter to {logic_type}")
        add_btn.clicked.connect(lambda: layout.insertLayout(
        layout.count() - 2, self._create_filter_row(logic_type, layout, group_box)
    ))
               
        #Make button stay at the bottom
        layout.addWidget(add_btn)
        layout.addStretch()

    
        group_box.setLayout(layout)
        return group_box

    
    def _create_filter_row(self, logic_type, parent_layout, logic_group_box, initial_field=None):
        row = QHBoxLayout()
    
        # Field selector
        field_selector = QComboBox()
        field_selector.addItems(self.filterable_fields)
        if initial_field:
            field_selector.setCurrentText(initial_field)
    
        # Operator selector
        op_selector = QComboBox()
        op_selector.setMinimumWidth(120)
    
        # Value input container
        value_input_container = QWidget()
        value_input_layout = QHBoxLayout()
        value_input_layout.setContentsMargins(0, 0, 0, 0)
        value_input_container.setLayout(value_input_layout)
    
    
        # Remove button
        remove_btn = create_button("❌")
        remove_btn.setFixedWidth(32)
        remove_btn.setFixedHeight(24)
        remove_btn.setStyleSheet("padding: 0px;")
    
        def remove_row():
            # Remove all widgets from the row
            for i in reversed(range(row.count())):
                widget = row.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            parent_layout.removeItem(row)
            self.update_query_preview()
    
            # If this group is now empty, remove the whole group
            if self._is_group_empty(parent_layout):
                self.filter_group_container.removeWidget(logic_group_box)
                logic_group_box.setParent(None)
                if logic_type == "OR":
                    self.add_or_btn.setVisible(True)
                elif logic_type == "NOT":
                    self.add_not_btn.setVisible(True)
    
        remove_btn.clicked.connect(remove_row)
    
        # Update logic when the selected field changes
        def update_filter_row_behavior():
            field = field_selector.currentText()
    
            # Update operator choices
            op_selector.clear()
            for code in self.supported_operators.get(field, ["EQ"]):
                label = next((k for k, v in self.condition_ops.items() if v == code), "Equals")
                op_selector.addItem(label)
    
            # Set default operator if defined
            default_op_code = self.default_operators.get(field, "EQ")
            default_label = next((k for k, v in self.condition_ops.items() if v == default_op_code), "Equals")
            op_selector.setCurrentText(default_label)
            # Clear previous input widgets
            for i in reversed(range(value_input_layout.count())):
                widget = value_input_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
    
            # Create default input widget: QLineEdit (comma-separated for multi-values)
            input_widget = self._create_value_input_by_field(field)
                
            if input_widget:
                input_widget.setMinimumWidth(150)
                value_input_layout.addWidget(input_widget)
                value_input_container.setLayout(value_input_layout)
                value_input_container.update()
                value_input_container.repaint() 
                
            self._connect_field_change(row)    
        
        # Live re-rendering when field changes
        field_selector.currentTextChanged.connect(update_filter_row_behavior)
        update_filter_row_behavior()
        
    
        # Assemble full row
        row.addWidget(field_selector)
        row.addWidget(op_selector)
        row.addWidget(value_input_container)
        row.addWidget(remove_btn)
        
        self._connect_field_change(row)
        return row
           
        
    def _remove_filter_row(self, row_layout, parent_layout, logic_type):
        # remove UI row
        for i in reversed(range(row_layout.count())):
            widget = row_layout.itemAt(i).widget()
        if widget:
            widget.setParent(None)
        parent_layout.removeItem(row_layout)
        
        # Remove Group if row = 0 in the Group
        filter_rows = [
            item for item in parent_layout.children() 
            if isinstance(item, QLayout) and item.count() > 0
        ]
        if len(filter_rows) == 0 and logic_type != "AND":
            self.filter_group_container.removeWidget(self.logic_groups[logic_type])
            self.logic_groups[logic_type].setParent(None)
            self.logic_groups.pop(logic_type)
            
        # Show button
        if logic_type == "OR":
            self.add_or_btn.setVisible(True)
        elif logic_type == "NOT":
            self.add_not_btn.setVisible(True)

    def _create_value_input_by_field(self, field_name):
        if field_name == "region_code":
            input_widget, combo, _, _ = create_multi_select_input(
                REGION_CODES,
                on_update=lambda: (
                    self.update_query_preview(),
                    focus_on_query_value(self.query_preview, ",".join(input_widget.selected_codes))
                    
                )
            )
            return input_widget
        
        elif field_name == "video_length":
            lengths = {
                "Short": "SHORT", "Mid": "MID",
                "Long": "LONG", "Extra Long": "EXTRA_LONG"
            }
            input_widget, combo, _, _ = create_multi_select_input(
                lengths,
                on_update=lambda: (
                    self.update_query_preview(),
                    focus_on_query_value(self.query_preview, ",".join(input_widget.selected_codes))
                )
            )
            return input_widget
        elif field_name == "create_time":
            input_widget = QDateEdit()
            input_widget.setCalendarPopup(True)
            input_widget.setDate(QDate.currentDate().addDays(-3))
            return input_widget
        else:
            input_widget = QLineEdit()
            if field_name in self.placeholder_map:
                input_widget.setPlaceholderText(self.placeholder_map[field_name])
            return input_widget
       
    def _create_date_range_row(self, group_layout, group_widget):

        # create_date_range_widget() → (layout widget, start QDateEdit, end QDateEdit)
        date_widget, start_date, end_date = create_date_range_widget()
    
        # Save status (self)
        self.start_date = start_date
        self.end_date = end_date
    
        # Validate Date range (within 30 days)
        self.end_date.dateChanged.connect(self.validate_date_range)
        
        # Layout
        wrapper = QHBoxLayout()
        wrapper.addWidget(date_widget)
    
        return wrapper
    
    def validate_date_range(self):
        max_days = 30
        days = self.start_date.date().daysTo(self.end_date.date())
        if days > max_days:
            QMessageBox.warning(self, "Invalid Date", f"End date must be within {max_days} days of start date.")
            self.end_date.setDate(self.start_date.date().addDays(max_days))

    def _is_group_empty(self, layout):
        count = 0
        for i in range(layout.count()):
            if isinstance(layout.itemAt(i), QHBoxLayout):
                    count += 1
        return count == 0
  
    def run_advanced_query(self):
        query = self.build_query()
    
        # 1. Save Query status
        self.current_query = query
        self.cursor = 0
        self.search_id = None
        self.loaded_data = []
    
        # 2. Update Live Preview 
        preview = self.query_preview
        if preview:
            preview.setPlainText(json.dumps(query, indent=2))
    
        # 3. Request API → Show result
        def fetch():
            if not   self.has_selected_fields():
                QMessageBox.warning(self, "Missing Fields", "Please select at least one field to include in the result.")
            return 
        
        self.api.fetch_videos_query(
                query_body=query,
                start_date=query["start_date"],
                end_date=query["end_date"],
                cursor=self.cursor,
                limit=100
            )
    
        def after_fetch(result):
            if result is None:
                return
            
            videos, has_more, cursor, search_id = result
            self.loaded_data.extend(videos)
            self.has_more = has_more
            self.cursor = cursor
            self.search_id = search_id
    
            self.update_table()
            self.show_advanced_result_layout()
    
        ProgressBar.run_with_progress(self, fetch, after_fetch)
            
            
    
    def show_advanced_result_layout(self):
        self.advanced_query_group.setVisible(False)
        self.advanced_result_group.setVisible(True)
    
    def restore_advanced_query_layout(self):
        self.advanced_result_group.setVisible(False)
        self.advanced_query_group.setVisible(True)
                   
                
    # def run_first_query(self):
    #     query = self.build_query()
        
    #     # 1. Query and Variables initialization
    #     self.current_query = query
    #     self.cursor = 0
    #     self.search_id = None
    #     self.loaded_data = []
        
    #     # 2. Call TikTok API
    #     def fetch_videos():
    #         print("⚠️ after_fetch reached")
    #         return self.api.fetch_videos_query(
    #             query_body=query,
    #             start_date=query["start_date"],
    #             end_date=query["end_date"],
    #             cursor=self.cursor,
    #             limit=100
    #             )
        
    #     # 3. Handling after API response
    #     def after_fetch(result):               
    #         videos, has_more, cursor, search_id, error_message = result
            
    #         if error_message:
    #             QMessageBox.critical(self, "TikTok API Error", error_message)
    #             return
            
    #         self.loaded_data.extend(videos)
            
    #         self.has_more = has_more
    #         self.cursor = cursor
    #         self.search_id = search_id
                        
    #         self.update_table()
    #         self.live_preview_group.hide()
    #         self.result_group.show()
            
           
    #         self.load_more_button.setVisible(has_more)

        
    #     ProgressBar.run_with_progress(self, fetch_videos, after_fetch)
    
    def _fetch_next_video_page(self):
        return self.api.fetch_videos_query(
            query_body=self.current_query,
            start_date=self.current_query["start_date"], 
            end_date=self.current_query["end_date"],
            cursor=self.cursor,
            limit=100,
            search_id=self.search_id
        )
    
    def load_more(self):
        def fetch_next():
            return self._fetch_next_video_page()

        def after_fetch(result):
            videos, has_more, cursor, search_id, error_message = result
            
            if error_message:
                QMessageBox.critical(self, "TikTok API Error", error_message)
                return
            
            self.loaded_data.extend(videos)
            
            self.has_more = has_more
            self.cursor = cursor
            self.search_id = search_id
            
            self.update_table()
            self.load_more_button.setVisible(has_more)

    
        ProgressBar.run_with_progress(self, fetch_next, after_fetch)
        
    def update_table(self): 
        import pandas as pd
        from queryFormatter import preferred_order_video
        
        df = pd.DataFrame(self.loaded_data)
        
        # Rearrange as "preferred order"
        ordered_columns = [col for col in preferred_order_video if col in df.columns]
        df = df[ordered_columns + [col for col in df.columns if col not in ordered_columns]]
        
        model = PandasModel(df)
        self.table.setModel(model)
        
        self.result_group.setVisible(True) # Only visible when there is a result (include result table)
        
        # Update (downloading) status
        self.total_loaded_label.setText(f"{len(self.loaded_data)} videos loaded.")
        self.update_load_status()
 
    def update_load_status(self):
        current = len(self.loaded_data)
        selected_text = self.max_results_selector.currentText()
        max_limit = "∞" if selected_text == "ALL" else selected_text
        self.load_status_label.setText(f" Loaded {current} / {max_limit}")
        
    def run_download_with_progress(self, file_format="csv", file_prefix="all"):
        selected_text = self.max_results_selector.currentText()
        limit = None if selected_text == "ALL" else int(selected_text)
    
        def task():
            try:
                all_data = self.loaded_data[:]  # include already loaded
                has_more = self.has_more
                cursor = self.cursor
                search_id = self.search_id
        
                while has_more and (limit is None or len(all_data) < limit):
                    result = self.api.fetch_videos_query(
                        query_body=self.current_query,
                        start_date=self.current_query["start_date"],
                        end_date=self.current_query["end_date"],
                        cursor=cursor,
                        limit=100,
                        search_id=search_id
                    )
                    
                    if isinstance(result, Exception):
                       raise result
                        
                    videos, has_more, cursor, search_id = result
                    all_data.extend(videos)
        
                if limit:
                    all_data = all_data[:limit]
        
                return all_data
            
            except Exception as e:
                return e
    
        def on_done(data):
            print("✅ on_done reached")
            print("⚠️ Exception detected:", str(data))
            
            from PyQt5.QtCore import QTimer
            if isinstance(data, Exception):
                msg = str(data)               
                user_message = get_friendly_error_message(msg)
                
                QTimer.singleShot(300, lambda: QMessageBox.critical(
                       self,
                       "TikTok API Error",
                       user_message,
                       QMessageBox.Ok
                ))
                return
            
            if not data:
                QMessageBox.information(self, "No Data", "No data available to download.")
                return
    
            FileProcessor().export_with_preferred_order(data, f"{file_prefix}_result", file_format)
            QMessageBox.information(self, "Download Complete", f"Your {file_format} file with {len(data)} items saved successfully.")
    
        ProgressBar.run_with_progress(self, task, on_done)
    
    def download_csv(self):
        self.run_download_with_progress("csv", file_prefix="video")
    
    def download_excel(self):
        self.run_download_with_progress("excel", file_prefix="video")
        
    
        
    # def clear_query(self):
 
        
    #     # Reset data pickers
    #     self.start_date.setDate(QDate.currentDate().addDays(-7))
    #     self.end_date.setDate(QDate.currentDate())
        
    #     # Clear region codes
    #     self.selected_region_codes.clear()
    #     self.region_display.setText("Selected: ")
    #     self.region_combo.setCurrentIndex(0)
    
    #     # Uncheck advanced field checkboxes only
    #     for field, cb in self.main_checkboxes.items():
    #         cb.setChecked(True)
    #     for cb in self.advanced_checkboxes.values():
    #         cb.setChecked(False)

    
    #     # Reset numeric filters
    #     for spinbox, combo in self.numeric_inputs.values():
    #         spinbox.setValue(0)
    #         combo.setCurrentText("Greater than")  # default value
    
    #     # Clear preview
    #     self.query_preview.clear()
    
    #     # Show live preview panel, hide result view
    #     self.live_preview_group.show()
    #     self.result_group.hide()
    #     self.load_more_button.setVisible(False)
        
    #     self.load_status_label.clear()
    #     self.total_loaded_label.clear()
        
    #     self.table.setModel(None) # Empty the Table
    #     self.loaded_data.clear() # Erase data in the Memory
        
    #     self.total_loaded_label.setText("No data loaded.")
    #     self.load_status_label.setText("")
        
    def has_selected_fields(self):
        return any(cb.isChecked() for cb in self.field_checkboxes.values())
    
    # Build query body : selected fields + And/Or/Not + start_date & end_date   
    def build_query(self):
        formatter = QueryFormatter()
    
        # 1. Selected fields
        included_fields = [f for f, cb in self.field_checkboxes.items() if cb.isChecked()]
    
        # 2. Filter logic groups
        clauses = []
    
        # each group is QGroupBox with title: "AND Filter Group", "OR Filter Group", "NOT Filter Group"
        for i in range(self.filter_group_container.count()):
            group_box = self.filter_group_container.itemAt(i).widget()
            if not isinstance(group_box, QGroupBox):
                continue
    
            logic_label = group_box.title().split()[0].upper()  # AND / OR / NOT
            group_layout = group_box.layout()
    
            # collect all filter conditions in this group
            conditions = []
            for j in range(group_layout.count()):
                item = group_layout.itemAt(j)
                if not item:
                    continue
                
                row = item.layout()
                if not isinstance(row, QHBoxLayout):  # This is a filter row
                    continue
                
                if row.count() < 3:
                    print("⚠️ Row has less than 3 widgets. Skipping.")
                    continue
    
                field_cb = row.itemAt(0).widget()
                op_cb = row.itemAt(1).widget()
                value_widget = row.itemAt(2).widget().layout().itemAt(0).widget()
                
                # Extract values
                field = field_cb.currentText()
                op_label = op_cb.currentText()
                op_code = self.condition_ops.get(op_label, "EQ")
    
                    # Extract input value depending on widget type
                if isinstance(value_widget, QLineEdit):
                    value = value_widget.text().strip()
                elif isinstance(value_widget, QDateEdit):
                    value = value_widget.date().toString("yyyyMMdd")
                elif isinstance(value_widget, QComboBox):
                    value = value_widget.currentText().strip()
                elif hasattr(value_widget, "selected_codes"):
                    value = ",".join(value_widget.selected_codes)
                else:
                    value = ""
    
                if value:
                    conditions.append((field, value, op_code))
    
            if conditions:
                if logic_label == "AND":
                    clause = formatter.query_AND_clause(conditions)
                elif logic_label == "OR":
                    clause = formatter.query_OR_clause(conditions)
                elif logic_label == "NOT":
                    clause = formatter.query_NOT_clause(conditions)
                clauses.append(clause)
    
        # 3. Combine into query body
        start_date = self.start_date.date().toString("yyyyMMdd")
        end_date = self.end_date.date().toString("yyyyMMdd")
    
        return {
            "fields": included_fields,
            **formatter.query_builder(start_date, end_date, clauses) # ** : unpacking and merge with fields
        }

    
# Field + Emoji + Explanation dict            
CREATOR_FIELDS = {
    "id": ("\U0001F194", "Unique video ID"),
    "username": ("\U0001F464", "Creator's username"),
    "region_code": ("\U0001F30D", "Region code of video"),
    "is_stem_verified": ("\U0001F9EA", "STEM Verified creator")
}

POSTING_FIELDS = {
    "create_time": ("\U0001F552", "Time when the video was posted"),
    "video_duration": ("\u23F1\uFE0F", "Duration of the video (sec)"),
    "video_description": ("\U0001F4DD", "Video caption"),
    "music_id": ("\U0001F3B5", "Music used in video"),
    "playlist_id": ("\U0001F4D6", "Playlist this video belongs to")
}

ENGAGEMENT_FIELDS = {
    "view_count": ("\U0001F441\uFE0F", "View count"),
    "like_count": ("\u2764\uFE0F", "Like count"),
    "comment_count": ("\U0001F4AC", "Comment count"),
    "share_count": ("\U0001F501", "Share count"),
    "favourites_count": ("\u2B50", "Favorite count")
}

TAGS_FIELDS = {
    "hashtag_names": ("\U0001F3F7\uFE0F", "Hashtags"),
    "video_label": ("\U0001F4CB", "Video labels"),
    "video_tag": ("\U0001F4CC", "Video tags"),
    "voice_to_text": ("\U0001F5E3\uFE0F", "Voice-to-text"),
    "video_mention_list": ("\U0001F465", "Mentioned users")
}

ADVANCED_FIELDS = {
    "effect_ids": ("\U0001F57A", "Visual effects used"),
    "effect_info_list": ("\U0001F3A8", "Effect metadata"),
    "hashtag_info_list": ("\U0001F4CA", "Hashtag metadata"),
    "sticker_info_list": ("\U0001F4D1", "Sticker metadata")
}



# # For testing
# if __name__ == "__main__":
#     import sys
#     from PyQt5.QtWidgets import QApplication
    
#     app = QApplication(sys.argv)
#     window = VideoQueryUI()
#     window.show()
#     sys.exit(app.exec())
   