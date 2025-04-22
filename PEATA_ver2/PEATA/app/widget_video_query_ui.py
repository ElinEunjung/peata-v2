# from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QComboBox, QTabWidget, QMessageBox, QCheckBox, QGroupBox, QLayout
    )
from widget_common_ui_elements import (
    create_date_range_widget, create_field_checkbox_group, create_result_table,
    create_collapsible_section, create_labeled_input,
    create_checkbox_with_tooltip, create_button,
    create_field_group_with_emojis, create_enum_checkbox_group, 
    create_numeric_filter_group, create_horizontal_line,
    create_scrollable_area, focus_on_query_value,
    create_multi_select_input_with_labels,
    create_result_control_panel,
    create_query_control_buttons, create_live_query_preview_panel
    )
from widget_region_codes import REGION_CODES
from widget_progress_bar import ProgressBar
from api import TikTokApi
from FileProcessor import FileProcessor
from widget_data_viewer import PandasModel
import json

""" TODO
Top Priorities (19 april)
- Check if I included all the fields? 
    "fields" : "id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,voice_to_text,is_stem_verified,video_duration,hashtag_info_list,video_mention_list,video_label"
- Do functionality test 
    fileProcessor.save_jason_to_csv(): Does file can save properly in FileProcessor?
    Does progress_bar work?
    Does data_viewer work?
    Test Max Result option
    

- Fix data viewer
- Include Help text in Field Tap (ex.Tip: Select all fields you want to include in the result. The API does not return unchecked fields)


Others

- Fix Region code checkbox update in Live preview panel
- Adapt async/thread for Cancel button/function
- Check value before excute run_query()
- Add operation parameter in query (not, or)
- Fix Tooltip for Music ID (do broad search include Music IDs)
- Fix basic styling
- Add field name explanation in Live Query Preview
- refactor code with common ui elements
- Add Help/Warning text in GUI

More styling
- Work with Live Query Preview - fix highlighter range
- Add color in JSON field

"""
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
    
    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_advanced_tab(), "Advanced")
        
        """
        Future expansion for simple mode!
        """
        # self.tabs.addTab(self.create_simple_tab(), "Simple")
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        
        
        # # Right panel: Live Preview Group(Scrollable Query Preview) + Result Table + Control Panel
        # right_panel = QVBoxLayout()        
        
        # self.query_preview = QTextEdit()
        # self.query_preview.setReadOnly(True)
        # self.query_preview.setMinimumHeight(200)
        # self.query_preview_scroll = create_scrollable_area(self.query_preview)
        
        # # Notice label (Move this to Style.qss!)
        # self.query_info_label = QLabel(
        #     'ℹ️ The API will <span style="color:#6c7ae0; font-weight:bold;"> ONLY RETURN </span> the fields you selected.')
        # self.query_info_label.setStyleSheet("color: #555; font-size: 10pt; padding-left: 5px;")
        
        # live_preview_layout = QVBoxLayout()
        # live_preview_layout.addWidget(self.query_info_label)
        
        # live_preview_layout.addWidget(self.query_preview_scroll)
        
        # self.live_preview_group = QGroupBox("🧠 Live Query Preview")
        # self.live_preview_group.setLayout(live_preview_layout)
        
        
        # right_panel.addWidget(self.live_preview_group)
                        
        # # Create Table (for Result)
        # self.table = create_result_table()
        
        # # Result control panel
        # self.result_control_panel, self.load_more_button, self.load_status_label, self.total_loaded_label = create_result_control_panel(
        # on_load_more=self.load_more,
        # on_download_csv=self.download_csv,
        # on_download_excel=self.download_excel,
        # on_back_to_query=self.restore_query_layout)
        
        # # Horizontla layout : Result Table + Result Control Panel
        # result_layout = QHBoxLayout()
        # table_layout = QVBoxLayout()
        # table_layout.addWidget(self.table)
        # result_layout.addLayout(table_layout, stretch=4)
        # result_layout.addWidget(self.result_control_panel, stretch=1)
    
        # self.result_group = QGroupBox("📊 Results")
        # self.result_group.setLayout(result_layout)
        
        # right_panel.addWidget(self.result_group)
        # self.result_group.setVisible(False) # Hide at first
        
        # # Wrap panels into main layout
        # main_layout.addLayout(left_panel, stretch=2)
        # main_layout.addLayout(right_panel, stretch=3) # Wider preview area       
        # self.setLayout(main_layout)
        
        # self.connect_live_query_signals()
        
        # self.update_query_preview()    # Update defalt view of Live Query Preview

    # def create_simple_tab(self):
    #     # Future expansion for simple mode!
    #     # simple query + simple result group
    #     pass
    
    def create_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
    
        self.advanced_query_group = self.create_advanced_query_group()
        # self.advanced_result_group = self.create_advanced_result_group()
        # self.advanced_result_group.setVisible(False) # Hide at first
    
        layout.addWidget(self.advanced_query_group)
        # layout.addWidget(self.advanced_result_group)
    
        tab.setLayout(layout)
        return tab
    
    def create_advanced_query_group(self):
        # Query Input UI : Query Group(Field + Filter + Preview)
        
        container = QWidget()
        main_layout = QHBoxLayout()  
    
        # LEFT: Field Selection + Filter Builder Query Control Buttons
        left_panel = QVBoxLayout()
        
        # Top row: Select Field + Fiter Buidler
        top_row_layout = QHBoxLayout()
        top_row_layout.addWidget(self.create_field_selection_panel())
        top_row_layout.addWidget(self.create_filter_builder_panel())        
        left_panel.addLayout(top_row_layout)
        
        # Bottom row: Excution / Initialization
        bottom_row_layout = QHBoxLayout()
        bottom_row_layout.addLayout(
    create_query_control_buttons(self.run_advanced_query, self.clear_query)
)
        left_panel.addLayout(bottom_row_layout)    
        
        left_container = QWidget()
        left_container.setLayout(left_panel)
        main_layout.addWidget(left_container, 3)
        
        # RIGHT: Live Query Preview
        self.live_preview_group = create_live_query_preview_panel()  # QGroupBox
        main_layout.addWidget(self.live_preview_group, 2)  
    
        container.setLayout(main_layout)        
        self.update_query_preview() # Show default query
        return container
        
    
    # def create_advanced_result_group(self):
    #     # Result table + Download
    #     pass    
    
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
        
        if logic_type == "AND" and include_base:
           layout.addLayout(self._create_filter_row(layout, group_box, "username", "EQ"))
           layout.addLayout(self._create_filter_row(layout, group_box, "keyword", "IN"))
           layout.addLayout(self._create_date_range_row(layout, group_box))
           layout.addLayout(self._create_filter_row(layout, group_box, "region_code", "IN"))
        else:
            layout.addLayout(self._create_filter_row(layout, group_box))
                       
        # Fixed button at the bottom
        add_btn = create_button(f"+ Add Filter to {logic_type}")
        add_btn.clicked.connect(lambda: layout.insertLayout(
        layout.count() - 1, self._create_filter_row(layout, group_box)
    ))
               
        #Make button stay at the bottom
        layout.addStretch()
        layout.addWidget(add_btn)
    
        group_box.setLayout(layout)
        return group_box

    def _add_filter_row_to_group(self, layout, logic_type: str):
            
            row = self._create_filter_row()
            layout.insertLayout(layout.count() - 2, row)  # -2 means before "stretch + button"

    
    def _create_filter_row(self, group_layout, group_widget, field=None, op_label="EQ", default_value=""):
        row = QHBoxLayout()
    
        field_selector = QComboBox()
        field_selector.addItems(self.all_supported_fields)
        if field:
            field_selector.setCurrentText(field)
    
        value_input = QLineEdit()
        value_input.setPlaceholderText("Enter value")
        value_input.setText(default_value)
    
        op_selector = QComboBox()
        op_selector.addItems(list(self.condition_ops.keys()))
        op_selector.setCurrentText(op_label)
    
        remove_btn = create_button("❌")
    
        def remove_row():
            for i in reversed(range(row.count())):
                widget = row.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            group_layout.removeItem(row)
    
            if self._is_group_empty(group_layout):
                self.filter_group_container.removeWidget(group_widget)
                group_widget.setParent(None)
                
                title = group_widget.title()
                if "OR" in title:
                    self.add_or_btn.setVisible(True)
                elif "NOT" in title:
                    self.add_not_btn.setVisible(True)
    
        remove_btn.clicked.connect(remove_row)
    
        row.addWidget(field_selector)
        row.addWidget(value_input)
        row.addWidget(op_selector)
        row.addWidget(remove_btn)
    
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

            
    def _create_date_range_row(self, group_layout, group_widget):
        layout = QHBoxLayout()

        # create_date_range_widget() → (layout widget, start QDateEdit, end QDateEdit)
        date_widget, start_date, end_date = create_date_range_widget()
    
        # Save status (self)
        self.start_date = start_date
        self.end_date = end_date
    
        # Validate Date range (within 30 days)
        self.end_date.dateChanged.connect(self.validate_date_range)
    
        # Remove button (Disabled / Undeletable field)
        remove_btn = create_button("❌")
        remove_btn.setDisabled(True)
        remove_btn.setFixedWidth(30)
    
        # Layout
        wrapper = QHBoxLayout()
        wrapper.addWidget(date_widget)
        wrapper.addWidget(remove_btn)
    
        return wrapper
    
    def validate_date_range(self):
        max_days = 30
        days = self.start_date.date().daysTo(self.end_date.date())
        if days > max_days:
            QMessageBox.warning(self, "Invalid Date", f"End date must be within {max_days} days of start date.")
            self.end_date.setDate(self.start_date.date().addDays(max_days))

    def _is_group_empty(self, group_layout):
        count = 0
        for i in range(group_layout.count()):
            item = group_layout.itemAt(i)
            if isinstance(item, QHBoxLayout):
                count += 1
        return count == 0
    


    
    def create_advanced_query_controls(self):
        #Left: Logic Group + Filter + Buttons
        pass
    
    def run_advanced_query(self):
        query = self.build_query()
    
        # 1. Save Query status
        self.current_query = query
        self.cursor = 0
        self.search_id = None
        self.loaded_data = []
    
        # 2. Update Live Preview 
        preview = self.live_preview_group.findChild(QTextEdit)
        if preview:
            preview.setPlainText(json.dumps(query, indent=2))
    
        # 3. Request API → Show result
        def fetch():
            return self.api.fetch_videos_query(
                query_body=query,
                start_date=query["start_date"],
                end_date=query["end_date"],
                cursor=self.cursor,
                limit=100
            )
    
        def after_fetch(result):
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
                   
            
    def create_filter_tab(self):
        
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 1. Username
        self.username_input = QLineEdit()
        layout.addWidget(create_labeled_input("Username(s):", self.username_input, "e.g. elin0615, ibrahim5367, amalie4802, oda1839"))
    
        # Horizontal Line before Keyword filters        
        layout.addWidget(create_horizontal_line())
        
        # 2. Keyword
        self.keyword_input = QLineEdit()
        layout.addWidget(create_labeled_input("Keywords:", self.keyword_input, "e.g. coffee, tea"))
    
        # Horizontal Line before Hashtag filters
        layout.addWidget(create_horizontal_line())
        
        # 3. Hashtag
        self.hashtag_input = QLineEdit()
        layout.addWidget(create_labeled_input("Hashtags:", self.hashtag_input, "e.g. music, dance"))
        
        # Horizontal Line before Date Range filters
        layout.addWidget(create_horizontal_line())
    
        # 4. Date Range
        self.date_widget, self.start_date, self.end_date = create_date_range_widget()
        layout.addWidget(self.date_widget)
        
        # Horizontal Line before Region filters
        layout.addWidget(create_horizontal_line())
        
        # 5. Region Code (Multi-Select)
        self.region_widget, self.region_combo, self.region_display, self.selected_region_codes = create_multi_select_input_with_labels(
            "Region(s):", self.region_codes, on_add_callback=self.update_query_preview
            )
        layout.addWidget(self.region_widget)
        
        # Horizontal Line before numeric filters
        layout.addWidget(create_horizontal_line())
    
        # 6. Numeric Filters
        self.numeric_fields = ["like_count", "view_count", "comment_count", "share_count"]
        layout.addWidget(QLabel("Numeric Filters:"))
        numeric_widget, self.numeric_inputs = create_numeric_filter_group(self.numeric_fields, list(self.condition_ops.keys()), default_op = "Greater than")
        layout.addWidget(numeric_widget)
    
        # Horizontal Line after numeric filters
        layout.addWidget(create_horizontal_line())
        
        # 7. Video Length
        length_group, self.length_checkboxes = create_enum_checkbox_group("Video Length", ["SHORT", "MID", "LONG", "EXTRA_LONG"])
        layout.addWidget(length_group)
    
        # 8. Music ID
        self.music_input = QLineEdit()
        layout.addWidget(create_labeled_input("Music IDs:", self.music_input, "e.g. 678123, 894562"))
        
        # Horizontal Line before Effect ID filters
        layout.addWidget(create_horizontal_line())
    
        # 9. Effect ID
        self.effect_input = QLineEdit()
        layout.addWidget(create_labeled_input("Effect IDs:", self.effect_input, "e.g. 9876, 1012"))

        # Horizontal Line before Max rates limit
        layout.addWidget(create_horizontal_line())
        
        # 10. Max rate option
        self.max_results_selector = QComboBox()
        self.max_results_selector.addItems(["100", "500", "1000", "ALL"])
        self.max_results_selector.setCurrentText("500")
        layout.addWidget(create_labeled_input("Max Results:", self.max_results_selector))
    
     
        tab.setLayout(layout)
        
        return tab
    
    # def add_query_control_buttons(self, parent_layout):
    #     self.run_button = create_button("Run Query", click_callback = self.run_first_query)
    #     self.clear_button = create_button("Clear Query", click_callback = self.clear_query)
        
    #     btn_layout = QHBoxLayout()
    #     btn_layout.addWidget(self.run_button)
    #     btn_layout.addWidget(self.clear_button)
        
    #     self.run_button.setObjectName("RunQueryButton")
    #     self.clear_button.setObjectName("ClearQueryButton")
        
    #     parent_layout.addLayout(btn_layout)
    
    def _connect_highlighted_input(self, widget, extract_fn):
        widget.textChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview,extract_fn(widget))
        ))
        
    def connect_live_query_signals(self):
        
        # Link to Live Query update (with highlight effect)
        self._connect_highlighted_input(self.username_input, lambda w: w.text().split(",")[-1].strip())
        self._connect_highlighted_input(self.keyword_input, lambda w: w.text().split(",")[-1].strip())
        self._connect_highlighted_input(self.hashtag_input, lambda w: w.text().split(",")[-1].strip())
        self._connect_highlighted_input(self.music_input, lambda w: w.text().split(",")[-1].strip())
        self._connect_highlighted_input(self.effect_input, lambda w: w.text().split(",")[-1].strip())
    
        self.start_date.dateChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.start_date.text())
        ))
        self.end_date.dateChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.end_date.text())
        ))
    
        for length in self.length_checkboxes:
            self.length_checkboxes[length].stateChanged.connect(lambda _, l=length: (
                self.update_query_preview(),
                focus_on_query_value(self.query_preview, l)
            ))
    
        for cb in self.main_checkboxes.values():
            cb.stateChanged.connect(self.update_query_preview)
        for cb in self.advanced_checkboxes.values():
            cb.stateChanged.connect(self.update_query_preview)
        for cb in self.length_checkboxes.values():
            cb.stateChanged.connect(self.update_query_preview)
    
        for spinbox, combo in self.numeric_inputs.values():
            spinbox.valueChanged.connect(self.update_query_preview)
            combo.currentIndexChanged.connect(self.update_query_preview)
               

    def build_query(self):
        
        # Selected Fields
        included_fields = [f for f, cb in self.main_checkboxes.items() if cb.isChecked()] + \
                          [f for f, cb in self.advanced_checkboxes.items() if cb.isChecked()]
    
        # Filter conditions
        conditions = []
        add_condition = lambda f, vals: conditions.append({
            "field_name": f,
            "operation": "IN",
            "field_values": vals
        }) if vals else None
    
        add_condition("username", [s.strip() for s in self.username_input.text().split(',') if s.strip()])
        add_condition("keyword", [s.strip() for s in self.keyword_input.text().split(',') if s.strip()])
        add_condition("hashtag_name", [s.strip() for s in self.hashtag_input.text().split(',') if s.strip()])
        add_condition("music_id", [s.strip() for s in self.music_input.text().split(',') if s.strip()])
        add_condition("effect_id", [s.strip() for s in self.effect_input.text().split(',') if s.strip()])
        add_condition("video_length", [k for k, cb in self.length_checkboxes.items() if cb.isChecked()])
    
        # region_code (Select all if nothing has selected)
        region_codes_to_use = self.selected_region_codes if self.selected_region_codes else list(self.region_codes.values())
        add_condition("region_code", region_codes_to_use)
            
        # Numeric filters
        for field, (spinbox, combo) in self.numeric_inputs.items():
            val = spinbox.value()
            op_label = combo.currentText()
            op_code = self.condition_ops.get(op_label, "GT")
            if val > 0:
                conditions.append({
                    "field_name": field,
                    "operation": op_code,
                    "field_values": [str(val)]
                })
    
        # Date Range
        start_date = self.start_date.date().toString("yyyyMMdd")
        end_date = self.end_date.date().toString("yyyyMMdd")
    
        # Final Query
        query = {
            "fields": included_fields,
            "query": {"and": conditions},
            "start_date": start_date,
            "end_date": end_date
        }
    
        return query    
    
    def update_query_preview(self):    
        query = self.build_query()
        
        preview = self.live_preview_group.findChild(QTextEdit)
        if preview :
            preview.setPlainText(json.dumps(query, indent=2))
        self.update_field_warning_label()
    
        
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
        
    
        
    def clear_query(self):
        # Clear QLineEdit fields
        self.username_input.clear()
        self.keyword_input.clear()
        self.hashtag_input.clear()
        self.music_input.clear()
        self.effect_input.clear()  
        
        # Reset data pickers
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.end_date.setDate(QDate.currentDate())
        
        # Clear region codes
        self.selected_region_codes.clear()
        self.region_display.setText("Selected: ")
        self.region_combo.setCurrentIndex(0)
    
        # Uncheck advanced field checkboxes only
        for field, cb in self.main_checkboxes.items():
            cb.setChecked(True)
        for cb in self.advanced_checkboxes.values():
            cb.setChecked(False)
        for cb in self.length_checkboxes.values():
            cb.setChecked(False)
    
        # Reset numeric filters
        for spinbox, combo in self.numeric_inputs.values():
            spinbox.setValue(0)
            combo.setCurrentText("Greater than")  # default value
    
        # Clear preview
        self.query_preview.clear()
    
        # Show live preview panel, hide result view
        self.live_preview_group.show()
        self.result_group.hide()
        self.load_more_button.setVisible(False)
        
        self.load_status_label.clear()
        self.total_loaded_label.clear()
        
        self.table.setModel(None) # Empty the Table
        self.loaded_data.clear() # Erase data in the Memory
        
        self.total_loaded_label.setText("No data loaded.")
        self.load_status_label.setText("")
        
    def has_selected_fields(self):
        return any(cb.isChecked() for cb in     self.main_checkboxes.values()) or \
           any(cb.isChecked() for cb in self.advanced_checkboxes.values())
           
    def update_field_warning_label(self):
        if self.has_selected_fields():
            self.query_info_label.setStyleSheet("color: #555; font-size: 10pt; padding-left: 5px;")
        else:
            self.query_info_label.setStyleSheet("color: red; font-size: 10pt; font-weight:bold; padding-left: 5px;")
 
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
   