import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDesktopWidget,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtCore import Qt

from navbar import Navbar

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project PEATA")
        self.resize(900, 900)  # Window size

        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.jpg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print("ERROR> icon.jpg not found!")

        self.center()  # Center the window
        self.load_stylesheet()
        self.load_font()

        # ───── Main horizontal layout (left + right) ─────
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # ───── Left box (Navbar) ─────
        self.navbar = Navbar()
        self.navbar.exit_clicked.connect(self.close)
        main_layout.addWidget(self.navbar)

        # ───── Right box (dynamic content) ─────
        self.content_area = QVBoxLayout()
        welcome_label = QLabel("Welcome to PEATA!")
        welcome_label.setAlignment(Qt.AlignCenter)
        self.content_area.addWidget(welcome_label)

        content_container = QWidget()
        content_container.setLayout(self.content_area)
        main_layout.addWidget(content_container)

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
