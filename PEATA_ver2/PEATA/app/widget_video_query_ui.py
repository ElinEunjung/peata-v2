# from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate, Qt, QTimer
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
import ast  


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
        # self._signals_connected = False
  
                
    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_advanced_tab(), "Advanced")
        
        """Future expansion for simple mode! """
        # self.tabs.addTab(self.create_simple_tab(), "Simple")
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        self.update_query_preview()
     
    # def showEvent(self, event):
    #     super().showEvent(event)
    
    #     if not hasattr(self, "_signals_connected"):
    #         self._signals_connected = True
    #         self.connect_live_query_signals()
    #         self.update_query_preview()
    
    def connect_live_query_signals(self):
        
        # Date range → Only update, No highlight
        self.start_date.dateChanged.connect(lambda: (
            self.update_query_preview()
        ))
        self.end_date.dateChanged.connect(lambda: (
            self.update_query_preview()
        ))
        
        # Field checkboxes change (only update, no highlight)
        for checkbox in self.field_checkboxes.values():
            checkbox.stateChanged.connect(self.update_query_preview)
 
            
    def _connect_highlighted_input(self, input_ref):
        if isinstance(input_ref, QLineEdit):
            input_ref.textChanged.connect(lambda: (
                self.update_query_preview(),
                focus_on_query_value(self.query_preview, input_ref.text())
            ))
    
        elif isinstance(input_ref, QComboBox):
            input_ref.currentTextChanged.connect(lambda: (
                self.update_query_preview(),
                focus_on_query_value(self.query_preview, input_ref.currentText())
            ))
    
        elif isinstance(input_ref, QDateEdit):
            input_ref.dateChanged.connect(lambda: (
                self.update_query_preview(),
                focus_on_query_value(self.query_preview, input_ref.date().toString("yyyyMMdd"))
            ))
                    
    def _connect_field_change(self, row_widget: QHBoxLayout):
    # Change filed_selector -> refresh row
        """Connect changes in a filter row to update live query preview and highlight values."""

        # Change Field selector  → update only preview
        if row_widget.field_selector:
            row_widget.field_selector.currentTextChanged.connect(self.update_query_preview)
         
        # Change Operator selector → update only preview
        if row_widget.op_selector:
            row_widget.op_selector.currentTextChanged.connect(self.update_query_preview)
         
        # Connet Value input widget
        if row_widget.value_input_ref:
            input_ref = row_widget.value_input_ref
         
            if isinstance(input_ref, QLineEdit):
                input_ref.textChanged.connect(lambda: (
                    self.update_query_preview(),
                    focus_on_query_value(self.query_preview, input_ref.text())
                ))
            elif isinstance(input_ref, QComboBox):
                input_ref.currentTextChanged.connect(lambda: (
                    self.update_query_preview(),
                    focus_on_query_value(self.query_preview, input_ref.currentText())
                ))
            elif isinstance(input_ref, QDateEdit):
                input_ref.dateChanged.connect(lambda: (
                    self.update_query_preview(),
                    focus_on_query_value(self.query_preview, input_ref.date().toString("yyyyMMdd"))
                ))
               
    
    def update_query_preview(self):
        # if not hasattr(self, "filter_group_container") or self.filter_group_container is None:
        #     return 
        # print("[DEBUG] update_query_preview() called")
        query = self.build_query()
        #print("[DEBUG] query built:", query)
        
        preview = self.query_preview
        if preview :
            preview.setPlainText(json.dumps(query, indent=2, ensure_ascii=False))
        # print("[DEBUG] preview: ", json.dumps(query, indent=2, ensure_ascii=False))
        
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
        bottom_row_layout.addLayout(
    create_query_control_buttons(self.run_advanced_query, self.clear_query)
)
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
        
        self.update_query_preview()
        self.connect_live_query_signals()

        
        return group
    
    def create_result_group_ui(self, mode="advanced"):
        container = QGroupBox("📊 Results (Advanced)")
        layout = QHBoxLayout()
                  
        panel = create_result_control_panel(
            on_load_more=self.load_more,
            on_download_csv=self.download_csv,
            on_download_excel=self.download_excel,
            on_back_to_query=self.restore_advanced_query_layout
)

        self.load_more_button = panel["load_more_button"]
        self.download_csv_button = panel["download_csv_button"]
        self.download_excel_button = panel["download_excel_button"]
        self.back_button = panel["back_button"]
        self.load_status_label = panel["load_status_label"]
        self.total_loaded_label = panel["total_loaded_label"]
        

        self.table = create_result_table()
        self.result_group_layout = panel["group"]
        
        layout.addWidget(self.table, 4)
        layout.addWidget(self.result_group_layout, 1)
        container.setLayout(layout)
        return container
        
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
       
        # Filter Group Box (Add AND/OR/NOT Group)
        filter_panel = QGroupBox("🧪 Filter Conditions to apply")
        main_layout = QVBoxLayout()
        
        
        self.filter_group_container = QVBoxLayout()
        self.logic_groups = {
                "AND": None,
                "OR": None,
                "NOT": None
            }         

        # ALWAYS create AND group (unable to delete)
        and_group = self.create_filter_group_ui("AND", include_base=True)
        self.logic_groups["AND"] = and_group
        self.filter_group_container.addWidget(and_group)
    
        
    
        # + Add Group button layout
        self.add_or_btn = create_button("+ Add OR Group", object_name="logic-group-btn")
        self.add_not_btn = create_button("+ Add NOT Group", object_name="logic-group-btn")
        self.add_or_btn.clicked.connect(self._handle_add_or_click)
        self.add_not_btn.clicked.connect(self._handle_add_not_click)
      
        
        
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.add_or_btn)
        btn_layout.addWidget(self.add_not_btn)
        
        #Add to main_layout
        filter_group_container_widget = QWidget()
        filter_group_container_widget.setLayout(self.filter_group_container)
        main_layout.addWidget(filter_group_container_widget)
        main_layout.addLayout(btn_layout)

        filter_panel.setLayout(main_layout)
        return filter_panel

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
        # AND : filter row (4) + Date Range + Add button
        # OR/NOT : filter row (1) + Add button
        group_box = QGroupBox(f"{logic_type} Filter Group")
        layout = QVBoxLayout()
        
        if logic_type == "AND":
            layout.addLayout(self._create_date_range_row(layout, group_box))
            layout.addWidget(self._create_filter_row(initial_field="username", parent_layout=layout, logic_group_box=group_box))
            layout.addWidget(self._create_filter_row(initial_field="keyword", parent_layout=layout, logic_group_box=group_box))
            layout.addWidget(self._create_filter_row(initial_field="create_time", parent_layout=layout, logic_group_box=group_box))
            layout.addWidget(self._create_filter_row(initial_field="region_code", parent_layout=layout, logic_group_box=group_box))
        else:
            layout.addWidget(self._create_filter_row(initial_field=None, parent_layout=layout, logic_group_box=group_box))
                       
        # Fixed button at the bottom
        add_btn = create_button(f"+ Add Filter to {logic_type}")
        add_btn.clicked.connect(lambda: self._add_filter_row_directly(group_box))
               
        # Make button stay at the bottom
        layout.addWidget(add_btn)        
        layout.addStretch()  # Empty space
        group_box.setLayout(layout)
        
        return group_box

    
    def _create_filter_row(
            self,
            initial_field=None,
            parent_layout=None,
            logic_group_box=None
            ):
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_widget.setLayout(row_layout)
    
        # Field selector
        field_selector = QComboBox()
        field_selector.addItems(self.filterable_fields)
        if initial_field:
            field_selector.setCurrentText(initial_field)
    
        # Operator selector
        op_selector = QComboBox()
        op_selector.setMinimumWidth(120)
    
    
        # Value Input Widget - for update value (live preview + highlight)
        field = field_selector.currentText()
        value_input_info = self._create_value_input_by_field(field) # To decide what widget to create
        value_input_widget = value_input_info["widget"]
        value_input_ref = value_input_info["ref"]

        # Value Input Container - for refresh layout
        value_input_container = QWidget()
        value_input_layout = QHBoxLayout()
        value_input_layout.setContentsMargins(0, 0, 0, 0)
        value_input_container.setLayout(value_input_layout)
        
        # Remove button
        remove_btn = create_button("❌")
        remove_btn.setFixedSize(32, 24) # Set button size (width, height)
        #remove_btn.setStyleSheet("padding: 0px;")
    
        # Save parent_layout & logic_group_box in the row_widget
        row_widget.parent_layout = parent_layout
        row_widget.logic_group_box = logic_group_box

        remove_btn.clicked.connect(lambda: self._remove_filter_row(row_widget))
        
        # Assemble layout
        row_layout.addWidget(field_selector)
        row_layout.addWidget(op_selector)
        row_layout.addWidget(value_input_container)
        row_layout.addWidget(remove_btn)
       
        # Attach important parts to row_widget
        row_widget.field_selector = field_selector
        row_widget.op_selector = op_selector
        row_widget.value_input_container = value_input_container
        row_widget.remove_button = remove_btn
        row_widget.value_input_widget = None
        row_widget.value_input_ref = None
       
               
        field_selector.currentTextChanged.connect(lambda: self._refresh_filter_row_layout(row_widget))

        # Initialize setting : Value Widget + Connect Live Preview
        self._refresh_filter_row_layout(row_widget)       
        
        # Initial connection
        if row_widget.value_input_ref:
            self._connect_highlighted_input(row_widget.value_input_ref)
       

        return row_widget
    
    def _add_filter_row_directly(self, group):
        if not group:
            return
        
        layout = group.layout()
        row_widget = self._create_filter_row(parent_layout=layout, logic_group_box=group)
        layout = group.layout()
        button_index = layout.count() - 2
        layout.insertWidget(button_index, row_widget)
        
        # Update Preview after add new filter row
        self.update_query_preview()
    
    def _handle_add_or_click(self):
        if self.logic_groups["OR"] is None:
            self.add_logic_group("OR")
        else:
            self._add_filter_row_directly(self.logic_groups["OR"])
    
    def _handle_add_not_click(self):
        if self.logic_groups["NOT"] is None:
            self.add_logic_group("NOT")
        else:
            self._add_filter_row_directly(self.logic_groups["NOT"])

    
    def _reset_value_input_widget(self, row_widget):
        """
        Reset the VALUE INPUT WIDGET in the filter row based on the selected field.
        Only manages the VALUE INPUT WIDGET itself.
        """
        field = row_widget.field_selector.currentText()

        # Clear all existing widgets from the value input container
        layout = row_widget.value_input_container.layout()
        while layout.count():
            widget = layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)
                
        #  Create new input widget based on field (receive as dict)
        input_info = self._create_value_input_by_field(field)
        input_widget = input_info["widget"]
        input_ref = input_info["ref"]
        
        # Save
        row_widget.value_input_widget = input_widget
        row_widget.value_input_ref = input_ref
            
        if input_widget:
            layout.addWidget(input_widget)
        
        if input_ref:
            self._connect_highlighted_input(input_ref)              
        
    def _refresh_filter_row_layout(self, row_widget):
        """
        Refresh the ENTIRE FILTER ROW LAYOUT based on the selected field.
        Update value input widget + operator choices.
       """
        field = row_widget.field_selector.currentText()
        
        # Reset value input widget
        self._reset_value_input_widget(row_widget)
        
        
        # Update operator choices
        row_widget.op_selector.clear()
        supported_ops = self.supported_operators.get(field, ["EQ"])
        for op_code in supported_ops:
            label = next((label for label, code in self.condition_ops.items() if code == op_code), "Equals")
            row_widget.op_selector.addItem(label)
     
        # Set default operator
        default_op_code = self.default_operators.get(field, "EQ")
        default_label = next((label for label, code in self.condition_ops.items() if code == default_op_code), "Equals")
        row_widget.op_selector.setCurrentText(default_label)
            
        
    def _remove_filter_row(self, row_widget):
        parent_layout = getattr(row_widget, "parent_layout", None)
        group_box = getattr(row_widget, "logic_group_box", None)
                       
        # remove filter row
        if parent_layout:
            parent_layout.removeWidget(row_widget)
        row_widget.setParent(None)
        self.update_query_preview()
             
        # check if this group still has any filter rows left (count only widget have field_selector attr)
        if group_box:
            remaining_rows = [
                parent_layout.itemAt(i).widget()
                for i in range(parent_layout.count())
                if parent_layout.itemAt(i).widget() and hasattr(parent_layout.itemAt(i).widget(), "field_selector")
        ]

            
            logic_type = group_box.title().split()[0].upper()
    
            #Only remove group if it's not AND group
            if not remaining_rows and logic_type != "AND":
            
                self.filter_group_container.removeWidget(group_box)
                group_box.setParent(None)
        
                if logic_type == "OR":
                    self.add_or_btn.setVisible(True)
                elif logic_type == "NOT":
                    self.add_not_btn.setVisible(True)
                # Update logic_groups after group deletion
                self.logic_groups[logic_type] = None
                
                
    def _create_value_input_by_field(self, field):
        """
        Create an appropriate input widget based on the selected field.
        Returns "widget" for UI, "ref" for live connection
        
        """

        if field in ["username", "keyword", "music_id", "video_id", "hashtag_name", "effect_ids"]:
            # Simple text input
            input_widget = QLineEdit()
            input_widget.setPlaceholderText(f"Enter {field} value")
            return {
                "widget": input_widget,
                "ref": input_widget  
            }
        
        elif field == "create_time":
            # Date input
            input_widget = QDateEdit()
            input_widget.setCalendarPopup(True)
            input_widget.setDisplayFormat("yyyy-MM-dd")         
            input_widget.setDate(QDate.currentDate())  # Set default to today
            return {
                "widget": input_widget,
                "ref": input_widget
            }
        
        elif field == "region_code":
            # Region codes as dropdown (assuming self.region_codes exists)
            widgets = create_multi_select_input(REGION_CODES, on_update=self.update_query_preview)
            self.region_code_widgets = widgets
            input_widget = widgets["container"]
            return {
                "widget": widgets["container"],
                "ref": widgets["combo"]
            }
    
        elif field == "video_length":
            # Video length categories as dropdown
            video_length_map = {
                "Short": "SHORT",
                "Mid": "MID",
                "Long": "LONG",
                "Extra Long": "EXTRA_LONG"
            }
            widgets = create_multi_select_input(video_length_map, on_update=self.update_query_preview)
            self.video_length_widgets = widgets
            input_widget = widgets["container"]
            return {
                "widget": widgets["container"],
                "ref": widgets["combo"] 
            }
        
        else:
            # Default fallback: simple text input
            input_widget = QLineEdit()
            input_widget.setPlaceholderText("Enter value")
            return {
                "widget": input_widget,
                "ref": input_widget
            }
      
    def _create_date_range_row(self, group_layout, group_widget):

        date_info = create_date_range_widget()
    
        # Save status (self)
        self.start_date = date_info["start"]
        self.end_date = date_info["end"]
    
        # Validate Date range (within 30 days)
        self.end_date.dateChanged.connect(self.validate_date_range)
        
        # Layout
        wrapper = QHBoxLayout()
        wrapper.addWidget(date_info["widget"])
    
        return wrapper
    
    def validate_date_range(self):
        max_days = 30
        start = self.start_date.date()
        end = self.end_date.date()
        
        if start.daysTo(end) > max_days:
            QMessageBox.warning(self, "Invalid Date", f"End date must be within {max_days} days of start date.")
            self.end_date.setDate(start.addDays(max_days))

    def _is_group_empty(self, layout):
        return not any(isinstance(layout.itemAt(i), QHBoxLayout) for i in range(layout.count()))
  
    def run_advanced_query(self):
        if not   self.has_selected_fields():
            QMessageBox.warning(self, "Missing Fields", "Please select at least one field to include in the result.")
            return 
    
        self.check_max_limit()
        
        selected_text = self.max_results_selector.currentText()
        limit = None if selected_text == "ALL" else int(selected_text)
    
        query = self.build_query()
    
        # Save Query status
        self.current_query = query
        self.cursor = 0
        self.search_id = None
        self.loaded_data = []
    
        self.update_query_preview()
    
        # Request API → Show result
        def fetch():
           return self.api.fetch_videos_query(
                query_body=self.current_query,
                start_date=self.current_query["start_date"],
                end_date=self.current_query["end_date"],
                cursor=self.cursor,
                limit=100,  
                search_id=self.search_id
        )
    
        def after_fetch(result):           
            videos, has_more, cursor, search_id, error_msg = result
            
            if error_msg:
                QMessageBox.critical(self, "TikTok API Error", error_msg)
                return
            
            if not videos:
               # No data found
               QMessageBox.information(self, "No Results", "No videos found for the selected filters.")
               return
            
            self.loaded_data.extend(videos)
            self.has_more = has_more
            self.cursor = cursor
            self.search_id = search_id
    
            # If the first page is empty and has more
            if len(self.loaded_data) == 0 and self.has_more:
                print("⚠️ First page empty, trying next page...")   
               
                self.load_more()
                return
            
            self.update_table()
            self.show_advanced_result_layout()
    
        ProgressBar.run_with_progress(self, fetch, after_fetch)
            
            
    
    def show_advanced_result_layout(self):
        self.advanced_query_group.setVisible(False)
        self.advanced_result_group.setVisible(True)
    
    def restore_advanced_query_layout(self):
        self.advanced_result_group.setVisible(False)
        self.advanced_query_group.setVisible(True)
                   

    
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
            
            print(f"[DEBUG] API returned:\, {result}") 
            
            
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
        self.total_loaded_label.setText(f"{len(self.loaded_data)} videos loaded.")
        self.update_load_status()
        self.load_more_button.setVisible(self.has_more)
 
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
        
                return all_data[:limit] if limit else all_data
            
            except Exception as e:
                return e
    
        def on_done(data):
            print("✅ on_done reached")
            print("⚠️ Exception detected:", str(data))           
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
                
    def clear_query(self):      
        
        # 1. Delete old Advanced Query Group
        if self.advanced_query_group:
            self.advanced_query_group.setParent(None)
            self.advanced_query_group.deleteLater()
    
        # 2. Recreate a fresh Advanced Query Group
        self.advanced_query_group = self.create_advanced_query_group_ui()
        self.tabs.widget(0).layout().insertWidget(0, self.advanced_query_group)
    
        # 3. Reset result table and data
        self.table.setModel(None)
        self.loaded_data.clear()
    
        # 4. Reset status labels
        self.total_loaded_label.setText("")
        self.load_status_label.setText("")
    
        # 5. Update Live Query Preview
        self.update_query_preview()

        
    def has_selected_fields(self):
        return any(cb.isChecked() for cb in self.field_checkboxes.values())
    
    def check_max_limit(self):
        val = self.max_results_selector.currentText()
        if self.over_limit_warning_checkbox.isChecked():
            if val == "ALL" or (val.isdigit() and int(val) == 1000):
                QMessageBox.warning(self, "Warning", "You are requesting a large number of results. This may hit rate limits.")
                
    # Build query body : selected fields + And/Or/Not + start_date & end_date   
    def build_query(self):
        # if not hasattr(self, "filter_group_container") or self.filter_group_container is None:
        # # return basic query if no filter_group_container
        #     return {
        #         "fields": ["id", "username", "region_code","create_time",
        #         "video_description", "video_duration", 
        #         "view_count", "like_count", "comment_count",
        #         "share_count", "favorites_count",
        #         "music_id", "playlist_id", "voice_to_text",
        #         "hashtag_names", "hashtag_info_list",
        #         "effect_ids", "effect_info_list", 
        #         "video_mention_list", "video_label",
        #         "video_tag", "is_stem_verified",
        #         "sticker_info_list"], 
        #     "query": {"and": []},
        #     "start_date": QDate.currentDate().addDays(-7).toString("yyyyMMdd"),
        #     "end_date": QDate.currentDate().toString("yyyyMMdd")
        # }
        
        
        formatter = QueryFormatter()
    
        # 1. Selected fields
        included_fields = [field for field, checkbox in self.field_checkboxes.items() if checkbox.isChecked()]
    
        # 2. Filter logic groups
        clauses = []
    
        # each group is QGroupBox with title: "AND Filter Group", "OR Filter Group", "NOT Filter Group"
        for i in range(self.filter_group_container.count()):
            group_box = self.filter_group_container.itemAt(i).widget()
            if not isinstance(group_box, QGroupBox):
                continue
    
            logic_type = group_box.title().split()[0].upper()  # AND / OR / NOT
            group_layout = group_box.layout()
    
            # collect all filter conditions in this group
            group_conditions = []
   
            # Extract input value depending on widget type
            for j in range(group_layout.count()):
                item = group_layout.itemAt(j)               
                widget = item.widget()
                
                if widget and hasattr(widget, "field_selector"):
                    field = widget.field_selector.currentText()
                    op_label = widget.op_selector.currentText()

                    # Get value
                    value_layout = widget.value_input_container.layout()
                    if value_layout is None:
                        continue
                    
                    value_widget = value_layout.itemAt(0).widget()
                    if not value_widget:
                        continue
                                       
                    if isinstance(value_widget, QLineEdit):
                        value = value_widget.text().strip()
                    elif isinstance(value_widget, QComboBox):
                        value = value_widget.currentText().strip()
                    elif isinstance(value_widget, QDateEdit):
                        value = value_widget.date().toString("yyyyMMdd")
                    elif hasattr(value_widget, "selected_codes"):
                        value = ",".join(value_widget.selected_codes)
 
                    else:
                        value = ""
    
    
                    if value:  # No add if no value
                        op_code = self.condition_ops.get(op_label, "EQ")
                        if "," in value:
                            value_list = [v.strip() for v in value.split(",") if v.strip()]
                        else:
                            value_list = [value.strip()]
                                             
                        group_conditions.append((field, value_list, op_code))
    
            # Add group to clauses
            if group_conditions:
                if logic_type == "AND":
                    clause = formatter.query_AND_clause(group_conditions)
                elif logic_type == "OR":
                    clause = formatter.query_OR_clause(group_conditions)
                elif logic_type == "NOT":
                    clause = formatter.query_NOT_clause(group_conditions)
                else:
                    continue
                clauses.append(clause)
    
        # Date Range
        start_date = self.start_date.date().toString("yyyyMMdd")
        end_date = self.end_date.date().toString("yyyyMMdd")
    
        # Final query
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
   