import os

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWidget


# ───── HoverIconButton class ─────
class HoverIconButton(QToolButton):
    def __init__(self, label, icon_default_path, icon_hover_path, icon_size, style, height):
        super().__init__()
        self.icon_default = QIcon(icon_default_path)
        self.icon_hover = QIcon(icon_hover_path)

        self.setText(label)
        self.setIcon(self.icon_default)
        self.setIconSize(icon_size)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setMinimumHeight(height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet(style)

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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.buttons = []  # Save buttons here (except Exit)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(15)

        # ───── Style and Paths ─────
        button_height = 80
        icon_size = QSize(64, 64)
        base_path = os.path.join(os.path.dirname(__file__), "assets")

        def icon_path(name, theme):
            return os.path.join(base_path, f"{name}_{theme}.svg")

        # icon_path = lambda name, theme: os.path.join(base_path, f"{name}_{theme}.svg")

        style = """
        QToolButton {
            background-color: #0078d7;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
        }
        QToolButton:hover {
            background-color: #005a9e;
        }
        QToolButton:pressed {
            background-color: #003f7d;
        }
        """

        def create_hover_button(label, icon_name, on_click=None, save_button=True):
            btn = HoverIconButton(
                label=label,
                icon_default_path=icon_path(icon_name, "dark"),
                icon_hover_path=icon_path(icon_name, "light"),
                icon_size=icon_size,
                style=style,
                height=button_height,
            )
            if on_click:
                btn.clicked.connect(on_click)
            if save_button:
                self.buttons.append(btn)
            return btn

        # ───── Buttons ─────
        layout.addWidget(create_hover_button("VIDEO QUERY", "icon_video", self.video_query_clicked.emit))
        layout.addWidget(create_hover_button("COMMENT\nQUERY", "icon_comments", self.comment_query_clicked.emit))
        layout.addWidget(create_hover_button("USER QUERY", "icon_user", self.user_query_clicked.emit))

        # Extra space before ABOUT US
        layout.addSpacerItem(QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(create_hover_button("ABOUT US", "icon_info", self.about_clicked.emit))

        # Extra space before EXIT
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Exit button (NOT disabled even when not logged in)
        exit_btn = create_hover_button("EXIT", "icon_exit", self.exit_clicked.emit, save_button=False)
        layout.addWidget(exit_btn)

        self.setLayout(layout)
        self.setFixedWidth(150)

    def set_logged_in(self, logged_in):
        """Enable/disable all buttons except Exit"""
        for btn in self.buttons:
            btn.setEnabled(logged_in)
            if logged_in:
                btn.setStyleSheet(
                    """
                    QToolButton {
                        background-color: #0078d7;
                        color: white;
                        padding: 10px;
                        border: none;
                        border-radius: 5px;
                        font-weight: bold;
                        text-align: center;
                    }
                    QToolButton:hover {
                        background-color: #005a9e;
                    }
                    QToolButton:pressed {
                        background-color: #003f7d;
                    }
                """
                )
            else:
                btn.setStyleSheet(
                    """
                    QToolButton {
                        background-color: #5a5a5a;
                        color: lightgrey;
                        padding: 10px;
                        border: none;
                        border-radius: 5px;
                        font-weight: bold;
                        text-align: center;
                    }
                """
                )
