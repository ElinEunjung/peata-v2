from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QGroupBox, QDateEdit, QProgressBar, QPushButton, QScrollArea, QWidget, QSizePolicy, 
    QFrame, QSpinBox, QComboBox, QTableView, QTextEdit
)
from PyQt5.QtCore import QDate, QTimer, Qt
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat, QColor
from widget_region_codes import get_flag_emoji
import os

# For general structure styling. Created this for reusable components in UI

# TODO: Refactor `create_labeled_input` to auto-create input widget internally
# Suggested function: create_text_input_row(label_text, placeholder)

def create_checkbox_with_tooltip(label_text: str, emoji: str, tooltip_text: str, checked=True):
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    checkbox = QCheckBox(f"{emoji} {label_text}")
    checkbox.setChecked(checked)
    checkbox.setToolTip(tooltip_text)
    layout.addWidget(checkbox)
    layout.addStretch()
    container = QWidget()
    container.setLayout(layout)
    return container, checkbox

def create_date_range_widget():
    start_label = QLabel("Start Date:")
    start_label.setFixedWidth(120)
    start_date = QDateEdit()
    start_date.setCalendarPopup(True)
    start_date.setDate(QDate.currentDate().addDays(-7))

    end_label = QLabel("End Date:")
    end_label.setFixedWidth(120)
    end_date = QDateEdit()
    end_date.setCalendarPopup(True)
    end_date.setDate(QDate.currentDate())

    layout = QHBoxLayout()
    layout.addWidget(start_label)
    layout.addWidget(start_date)
    layout.addSpacing(20)
    layout.addWidget(end_label)
    layout.addWidget(end_date)

    container = QWidget()
    container.setLayout(layout)
    return {
        "widget": container,
        "start": start_date,
        "end": end_date
    }


def create_field_checkbox_group(fields):
    group_box = QGroupBox("Select Fields")
    layout = QVBoxLayout()
    checkboxes = {}

    for field in fields:
        cb = QCheckBox(f"{field}")
        checkboxes[field] = cb
        layout.addWidget(cb)

    group_box.setLayout(layout)
    return group_box, checkboxes


def create_result_table():
    table = QTableView()
    table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return table


def create_progress_bar():
    bar = QProgressBar()
    bar.setRange(0, 0)  # Infinite animation
    bar.setVisible(True)
    return bar

# For Advanced filters (less used options)
def create_collapsible_section(title: str, widget: QWidget, checked =True, on_toggle_callback=None):
    container = QGroupBox(title)
    container.setCheckable(True)
    container.setChecked(checked)
    
    layout = QVBoxLayout()
    layout.addWidget(widget)
    container.setLayout(layout)
    
    # Connect to Signal : If main advanced filter are unchecked, all children checkboxes are unchecked and update live query preview
    def handle_groupbox_toggled(state):
        for cb in widget.findChildren(QCheckBox):
            cb.setChecked(state)
        if on_toggle_callback:
            on_toggle_callback()
            
    container.toggled.connect(handle_groupbox_toggled)        
        
    return container

# For various fields (text box, dropdown etc)
def create_labeled_input(label_text: str, input_widget: QWidget, placeholder: str = ""):
    label = QLabel(label_text)
    if hasattr(input_widget, 'setPlaceholderText'):
        input_widget.setPlaceholderText(placeholder)
    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(input_widget)
    container = QWidget()
    container.setLayout(layout)
    return container

# For checkboxes in Advanced Options
def create_scrollable_area(content: QWidget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(content)
    return scroll


def create_horizontal_line():
    line = QFrame()
    line.setObjectName("HorizontalLine")
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Plain)   
    return line

def create_button(
        text: str, 
        object_name: str = "", 
        tooltip: str = "", 
        icon_path: str = "", 
        click_callback=None
        ):
    
    button = QPushButton(text)
    if object_name:
        button.setObjectName(object_name)
    if tooltip:
        button.setToolTip(tooltip)
    if icon_path and os.path.exists(icon_path):
        button.setIcon(QIcon(icon_path))
    if click_callback:
        button.clicked.connect(click_callback)
    return button

def create_field_group_with_emojis(
        title: str, fields: dict, store_dict: dict, default_checked=True
        ):
    
    group = QGroupBox(title)
    vbox = QVBoxLayout()
    for field, (emoji, tooltip) in fields.items():
        checkbox = QCheckBox(f"{emoji} {field.replace('_', ' ').title()}")
        checkbox.setToolTip(tooltip)
        checkbox.setChecked(default_checked)
        store_dict[field] = checkbox
        vbox.addWidget(checkbox)
    group.setLayout(vbox)
    return group

# def create_enum_checkbox_group(title: str, enum_values: list, default_checked=True):
#     group_box = QGroupBox(title)
#     layout = QVBoxLayout()
#     checkboxes = {}
#     for val in enum_values:
#         cb = QCheckBox(val)
#         cb.setChecked(default_checked)
#         layout.addWidget(cb)
#         checkboxes[val] = cb
#     group_box.setLayout(layout)
#     return group_box, checkboxes

# def create_numeric_filter_group(fields: list, operators: list, default_op="GT"):
#     numeric_inputs = {}
#     layout = QVBoxLayout()
    
#     for field in fields:
#         hbox = QHBoxLayout()
#         label = QLabel(field.replace("_", " ").title())
#         spinbox = QSpinBox()
#         spinbox.setMaximum(1_000_000)
#         spinbox.setMinimum(0)
        
#         op_selector = QComboBox()
#         op_selector.addItems(operators)
#         op_selector.setCurrentText(default_op)
        
#         hbox.addWidget(label)
#         hbox.addWidget(spinbox)
#         hbox.addWidget(op_selector)
#         container = QWidget()
#         container.setLayout(hbox)
#         layout.addWidget(container)
#         numeric_inputs[field] = (spinbox, op_selector)
#     container_widget = QWidget()
#     container_widget.setLayout(layout)
#     return container_widget, numeric_inputs

def focus_on_query_value(text_edit: QTextEdit, value_str):
    """
    Highlight a specific value in the Live Query Preview without affecting other text.
    - Only the target text will be highlighted with red background.
    - Scroll automatically to bring the target into view.
    """
    
    if value_str is None: 
        return 
    
    # Always treat value as string
    value_str = str(value_str).strip()
    
    if not value_str:
        return 
    
    plain_text = text_edit.toPlainText()
    target = f'"{value_str}"'
    
    index = plain_text.find(target)
    
    if index == -1:
        return # No change if there is no relevant value

    # Move cursor to target
    highlight_cursor = text_edit.textCursor()
    highlight_cursor.setPosition(index)
    highlight_cursor.setPosition(index + len(target), QTextCursor.KeepAnchor)
    
    # Highlight target only (Red + white)
    highlight_format = QTextCharFormat()
    highlight_format.setBackground(QColor("yellow"))
    highlight_format.setForeground(QColor("black"))
    
    highlight_cursor.mergeCharFormat(highlight_format)
    
    # Scroll to target
    text_edit.setTextCursor(highlight_cursor)
    text_edit.ensureCursorVisible()   

    # Remove highlight effect after 1 sec
    def clear_highlight():
        highlight_cursor.setPosition(index)
        highlight_cursor.setPosition(index + len(target), QTextCursor.KeepAnchor)
        clear_format = QTextCharFormat()
        clear_format.setBackground(QColor("transparent"))
        highlight_cursor.mergeCharFormat(clear_format)

    QTimer.singleShot(1000, clear_highlight)

# Multi-select using QComboBox + Add button 
def create_multi_select_input( name_code_map: dict, on_update=None):
    
    combo = QComboBox()
    combo.setEditable(True) # Allow manual typing/searching
    
    display_to_code = {}
    for name, code in name_code_map.items():
        display_text = f"{get_flag_emoji(code)} {name}"  if len(code) == 2 else name
        combo.addItem(display_text)
        display_to_code[display_text] = code  # internal mapping
        
    add_btn = QPushButton("Add")  
    selected_codes = []    
       
    def add_value():
        display_text = combo.currentText().strip()
        code = display_to_code.get(display_text, display_text) # Allow manual typing
        
        if code and code not in selected_codes: 
            # Consider text as code for manual typing
            selected_codes.append(code)
            
        # For Preivew update  
        if on_update:
            on_update()
        return code 
    
    add_btn.clicked.connect(add_value)

    layout = QHBoxLayout()
    layout.addWidget(combo)
    layout.addWidget(add_btn)

    container = QWidget()
    container.setLayout(layout)
    container.selected_codes = selected_codes
    
    return {
        "container": container,
        "combo": combo,
        "selected_codes": selected_codes,
        "add_value_func": add_value
    }

def create_result_control_panel(on_load_more, on_download_csv, on_download_excel, on_back_to_query):
    control_group = QGroupBox("📥 Query Result Controls")
    layout = QVBoxLayout()

    # Create button and status label
    load_more_button = QPushButton("🔄 Load More")
    load_more_button.setToolTip("Click to fetch the next page of results")
    load_more_button.clicked.connect(on_load_more)
    load_more_button.setVisible(False)

    download_csv_button = QPushButton("⬇️ All (CSV)")
    download_csv_button.clicked.connect(on_download_csv)

    download_excel_button = QPushButton("⬇️ All (Excel)")
    download_excel_button.clicked.connect(on_download_excel)
    
    back_button = QPushButton("Back to Query")
    back_button.clicked.connect(on_back_to_query) 
    
   
    load_status_label = QLabel("")
    total_loaded_label = QLabel("")
    total_loaded_label.setStyleSheet("font-size: 10pt; color: #555; padding: 4px;")
    total_loaded_label.setAlignment(Qt.AlignCenter)

    # Button layout
    button_layout = QVBoxLayout()
    button_layout.addWidget(load_more_button)
    button_layout.addWidget(download_csv_button)
    button_layout.addWidget(download_excel_button)
    button_layout.addWidget(back_button)

    layout.addLayout(button_layout)
    layout.addWidget(load_status_label)
    layout.addWidget(total_loaded_label)

    control_group.setLayout(layout)

    # Return as dict
    return {
        "group": control_group, 
        "load_more_button": load_more_button,
        "download_csv_button": download_csv_button,
        "download_excel_button": download_excel_button,
        "back_button": back_button,
        "load_status_label": load_status_label,
        "total_loaded_label": total_loaded_label,
        
        }

def create_query_control_buttons(run_callback, clear_callback):
    run_button = create_button("Run Query", object_name="RunQueryButton", click_callback=run_callback)
    clear_button = create_button("Clear Query", object_name="ClearQueryButton", click_callback=clear_callback)

    layout = QHBoxLayout()
    layout.addWidget(run_button)
    layout.addWidget(clear_button)

    return layout

def create_live_query_preview_panel(preview_label: str = "Live Query Preview") -> dict:
    
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)
    text_edit.setMinimumHeight(200)
    
    scrollable = create_scrollable_area(text_edit)

    layout = QVBoxLayout()
    layout.addWidget(scrollable)

    group = QGroupBox("🧠 " + preview_label)
    group.setLayout(layout)

    return {
        "group" : group,
        "text_edit" : text_edit
    }

def create_max_results_selector(label: str = "Max Results:") -> tuple[QGroupBox, QComboBox, QCheckBox]:

    selector = QComboBox()
    selector.addItems(["100", "500", "1000", "ALL"])
    selector.setCurrentText("500")
    selector.setToolTip("Maximum number of results to fetch. 'ALL' may take longer.")

    checkbox = QCheckBox("Warn if result count exceeds 1000")
    checkbox.setChecked(True)
    checkbox.setToolTip("Disable this if you want to skip warnings for large requests.")

    layout = QVBoxLayout()
    layout.addWidget(QLabel(label))
    layout.addWidget(selector)
    layout.addWidget(checkbox)

    group = QGroupBox("📊 Max Result Option")
    group.setLayout(layout)
    return group, selector, checkbox

    