import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDesktopWidget,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtCore import Qt

from navbar import Navbar
from about_us import AboutUs

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project PEATA | Home")
        self.resize(1000, 900)
        self.setMinimumSize(800, 700)

        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.jpg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print("ERROR> icon.jpg not found!")

        self.center()
        self.load_stylesheet()
        self.load_font()

        # ───── Main horizontal layout ─────
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # ───── Left box (Navbar) ─────
        self.navbar = Navbar()
        self.navbar.about_clicked.connect(self.show_about_us)
        self.navbar.exit_clicked.connect(self.close)
        self.main_layout.addWidget(self.navbar)

        # ───── Right box (Content) ─────
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_container.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_container)

        self.show_welcome_message()

    def show_welcome_message(self):
        self.setWindowTitle("Project PEATA | Home")
        self.clear_content()
        welcome_label = QLabel("Welcome to PEATA!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.content_layout.addWidget(welcome_label)

    def show_about_us(self):
        self.setWindowTitle("Project PEATA | About Us")
        self.clear_content()
        about_us_widget = AboutUs()
        self.content_layout.addWidget(about_us_widget)

    def clear_content(self):
        """Helper function to clear right content area"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as file:
                self.setStyleSheet(file.read())
        else:
            print("ERROR> style.qss not found!")

    def load_font(self):
        font_path = os.path.join(os.path.dirname(__file__), "assets", "font_tiktok.ttf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                QApplication.setFont(QFont(family, 11))  # Set globally
                print(f"Font loaded: {family}")
            else:
                print("ERROR> Failed to load TikTok font!")
        else:
            print("ERROR> font_tiktok.ttf not found!")

    def center(self):
        frame_geom = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(screen_center)
        self.move(frame_geom.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
