"""
Defines the vertical navigation bar with signal-enabled hover buttons.

Original Author: Ibrahim
Refactored & documented by : Elin
Date: 2025-06-28
Version: v2.0.0
"""

import os

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWidget


# ───── HoverIconButton class ─────
class HoverIconButton(QToolButton):
    def __init__(self, label, icon_default_path, icon_hover_path, icon_size, height):
        super().__init__()
        self.icon_default = QIcon(icon_default_path)
        self.icon_hover = QIcon(icon_hover_path)

        self.setText(label)
        self.setIcon(self.icon_default)
        self.setIconSize(icon_size)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setMinimumHeight(height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def enterEvent(self, event):
        if self.isEnabled():
            self.setIcon(self.icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self.setIcon(self.icon_default)
        super().leaveEvent(event)


# ───── Navbar Widget ─────
class Navbar(QWidget):
    about_clicked = pyqtSignal()
    exit_clicked = pyqtSignal()
    video_query_clicked = pyqtSignal()
    comment_query_clicked = pyqtSignal()
    user_query_clicked = pyqtSignal()

    def __init__(self, icon_size=QSize(64, 64), button_height=80, parent=None):
        super().__init__(parent)

        self.buttons = []  # Save buttons here (except Exit)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(15)

        # ───── Style and Paths ─────
        self.button_height = button_height
        self.icon_size = icon_size
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets")

        def icon_path(name, theme):
            return os.path.join(base_path, f"{name}_{theme}.svg")

        def create_hover_button(label, icon_name, on_click=None, save_button=True):
            btn = HoverIconButton(
                label=label,
                icon_default_path=icon_path(icon_name, "dark"),
                icon_hover_path=icon_path(icon_name, "light"),
                icon_size=icon_size,
                height=button_height,
            )
            if on_click:
                btn.clicked.connect(on_click)
            if save_button:
                self.buttons.append(btn)

            label_key = label.lower().replace(" ", "_").replace("\n", "_")
            btn.setObjectName(f"{label_key}_btn")  # VIDEO QUERY -> video_query_btn
            return btn

        # ───── Buttons ─────
        layout.addWidget(create_hover_button("VIDEO\nQUERY", "icon_video", self.video_query_clicked.emit))
        layout.addWidget(create_hover_button("COMMENT\nQUERY", "icon_comments", self.comment_query_clicked.emit))
        layout.addWidget(create_hover_button("USER\nQUERY", "icon_user", self.user_query_clicked.emit))

        # Extra space before ABOUT US
        layout.addSpacerItem(QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(create_hover_button("ABOUT US", "icon_info", self.about_clicked.emit))

        # Extra space before EXIT
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Exit button (NOT disabled even when not logged in)
        exit_btn = create_hover_button("EXIT", "icon_exit", self.exit_clicked.emit, save_button=False)
        layout.addWidget(exit_btn)

        self.setLayout(layout)
        self.setFixedWidth(130)
