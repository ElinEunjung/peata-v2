"""
Main application entry point for PEATA, initializing the GUI layout, login flow, and core query panels.

Original Author: Ibrahim
Refactored & documented by : Elin
Date: 2025-06-28
Version: v2.0.0
"""

import os
import platform
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from app import AboutUs, CommentQueryUI, LoginWidget, Navbar, TikTokApi, UserInfoQueryUI, VideoQueryUI, __version__


def resource_path(relative_path):
    """Get absolute path to resource (supports PyInstaller bundle and dev mode)."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        print(f"Launching PEATA v{__version__}")
        super().__init__()

        self.setWindowTitle("Project PEATA | Home")
        self.resize(1000, 900)
        self.setMinimumSize(800, 700)

        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "app", "assets", "peata.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print("ERROR> peata.ico not found!")

        self.center()
        self.load_stylesheet()
        self.load_font()

        # ───── Main horizontal layout ─────
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout()
        central_widget.setLayout(self.main_layout)

        # ───── Left box (Navbar) ─────
        self.navbar = Navbar(icon_size=icon_size, button_height=button_height)
        for btn in self.navbar.buttons:
            btn.setEnabled(False)
        self.navbar.about_clicked.connect(self.show_about_us)
        self.navbar.exit_clicked.connect(self.close)
        self.navbar.video_query_clicked.connect(self.show_video_query)
        self.navbar.comment_query_clicked.connect(self.show_comment_query)
        self.navbar.user_query_clicked.connect(self.show_user_query)
        self.main_layout.addWidget(self.navbar)

        # ───── Right box (Content) ─────
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_container.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_container)

        # ───── Show Login First ─────
        self.login_widget = LoginWidget()
        self.login_widget.login_successful.connect(self.handle_login_success)
        self.content_layout.addWidget(self.login_widget)

        # Placeholder variables
        self.api = None
        self.client_id = None
        self.client_key = None
        self.client_secret = None
        self.token = None

    def handle_login_success(self, client_id, client_key, client_secret, token):
        """When login is successful"""
        for btn in self.navbar.buttons:
            btn.setEnabled(True)

        # Save login credentials
        self.client_id = client_id
        self.client_key = client_key
        self.client_secret = client_secret
        self.token = token

        try:
            self.api = TikTokApi(self.client_key, self.client_secret, self.token)
        except Exception as e:
            QMessageBox.critical(self, "API Error", f"Failed to initialize TikTok API:\n{str(e)}")
            return

        self.show_welcome_message()
        print("✅ Login successful!")
        print(f"Client ID: {self.client_id}")
        print(f"Client Key: {self.client_key}")
        print(f"Client Secret: {self.client_secret}")
        print(f"Access Token: {self.token}")

    def show_welcome_message(self):
        self.setWindowTitle("Project PEATA | Home")
        self.clear_content()

        welcome_label = QLabel("Welcome to PEATA Data processor!")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(welcome_label)

    def show_about_us(self):
        self.setWindowTitle("Project PEATA | About Us")
        self.clear_content()

        about_us_widget = AboutUs()
        self.content_layout.addWidget(about_us_widget)

    def show_video_query(self):
        if not self.api:
            QMessageBox.warning(self, "Error", "API client not available. Please login.")
            return

        self.setWindowTitle("Project PEATA | Video Query")
        self.clear_content()

        widget = VideoQueryUI(api=self.api)
        self.content_layout.addWidget(widget)

    def show_comment_query(self):
        if not self.api:
            QMessageBox.warning(self, "Error", "API client not available. Please login.")
            return

        self.setWindowTitle("Project PEATA | Comment Query")
        self.clear_content()

        widget = CommentQueryUI(api=self.api)
        self.content_layout.addWidget(widget)

    def show_user_query(self):
        if not self.api:
            QMessageBox.warning(self, "Error", "API client not available. Please login.")
            return

        self.setWindowTitle("Project PEATA | User Info Query")
        self.clear_content()

        widget = UserInfoQueryUI(api=self.api)
        self.content_layout.addWidget(widget)

    def clear_content(self):
        """Helper function to clear right content area"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def center(self):
        frame_geom = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(screen_center)
        self.move(frame_geom.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ───── Scale font size based on resolution ─────
    screen = app.primaryScreen()
    w, h = screen.size().width(), screen.size().height()
    if w <= 1600:
        scale_factor = 0.85
        button_height = 64
        icon_size = QSize(48, 48)
    else:
        scale_factor = 1.0
        button_height = 80
        icon_size = QSize(64, 64)

    dpi = screen.logicalDotsPerInch()
    size = screen.size()
    print("DEBUG> DPI:", dpi, "| Resolution:", size.width(), "x", size.height())

    # ───── Determine icon path based on OS ─────
    if platform.system() == "Darwin":
        icon_path = resource_path("app/assets/peata_mac.icns")
    else:
        icon_path = resource_path("app/assets/peata_win.ico")

    # ───── Set window icon with correct platform icon ─────
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        print("ERROR> peata icon is not found!")

    # ───── Set Font ─────
    font_path = resource_path("app/assets/font_tiktok.ttf")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(family)
            font.setPointSizeF(15 * scale_factor)  # Base 15 pt scaled
            app.setFont(font)
            print(f"Font loaded: {family}")
        else:
            print("ERROR> Failed to load TikTok font!")
    else:
        print("ERROR> font_tiktok.ttf not found!")
    font = app.font()
    font.setPointSizeF(font.pointSizeF() * scale_factor)
    app.setFont(font)

    # ───── Set StyleSheet ─────
    qss_path = resource_path("app/view/style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print("ERROR> style.qss not found at", qss_path)

    # ───── Main Window ─────
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
