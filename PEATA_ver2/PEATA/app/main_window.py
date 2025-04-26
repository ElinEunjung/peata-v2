import sys
import os

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtCore import Qt

# ───── Widgets ─────
# (these imports are fine because no QWidget is created yet)
from PEATA_ver2.PEATA.app.navbar_OLD import Navbar
from about_us import AboutUs

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window icon and title
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.jpg")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Project PEATA | Home")
        self.setGeometry(100, 100, 700, 700)

        # ───── Main horizontal layout (Left navbar + Right content) ─────
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        # ───── Left: Navbar ─────
        self.navbar = Navbar()
        self.navbar.about_clicked.connect(self.show_about_us)
        self.navbar.exit_clicked.connect(self.close)
        main_layout.addWidget(self.navbar)

        # ───── Right: Content Window ─────
        self.content_window = QVBoxLayout()

        # Welcome message
        welcome_label = QLabel("Welcome to the PEATA experience")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)

        self.content_window.addWidget(welcome_label)

        content_container = QWidget()
        content_container.setLayout(self.content_window)
        main_layout.addWidget(content_container)

    def show_about_us(self):
        """Replace the content with the About Us page."""
        self.setWindowTitle("Project PEATA | About Us")

        # Clear previous widgets
        while self.content_window.count():
            item = self.content_window.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Add AboutUs widget
        self.content_window.addWidget(AboutUs())

# ───── Main Entry Point ─────
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load custom TikTok-style font
    font_path = os.path.join(os.path.dirname(__file__), "assets", "font_tiktok.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(family, 11))  # Optional: adjust font size
    else:
        print("ERROR, failed to load font")

    # Create and show the main window
    window = Window()
    window.show()

    sys.exit(app.exec_())
