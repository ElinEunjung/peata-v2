"""
Displays app introduction, usage guide, developer credits, and version info in the 'About Us' section.

Original Author: Ibrahim
Refactored & documented by : Elin
Date: 2025-06-28
Version: v2.0.0
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFormLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from app import __version__


class AboutUs(QWidget):
    def __init__(self):
        super().__init__()

        # Create scroll area
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        # Content inside the scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(30)

        # ───── Title and Intro ─────
        title = QLabel("{ About This App }")
        title.setObjectName("aboutTitle")
        title.setAlignment(Qt.AlignCenter)

        title_text = QLabel(
            '"Packages for Easier Access To APIs", or PEATA\n'
            "is a lightweight desktop tool designed to help users\n"
            "explore and analyze public TikTok Research API data.\n\n"
            "With a clean interface and customizable search options,\n"
            "PEATA makes it easy to query and view information about\n"
            "videos, comments and users(creators).\n\n"
            "PEATA helps researchers gather insights quickly and efficiently.\n\n"
        )
        title_text.setObjectName("aboutText")
        content_layout.addWidget(title)
        content_layout.addWidget(title_text)

        # ───── How to Use ─────
        howtoTitle = QLabel("{ How to Use This App }")
        howtoTitle.setObjectName("howtoTitle")
        howtoTitle.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(howtoTitle)

        howtoText = QLabel(
            "VIDEO QUERY - Press the button on the left if you want to query for videos.\n\n"
            "COMMENT QUERY - Press the button on the left if you want to query for comments.\n\n"
            "USER INFO QUERY - Press the button on the left if you want to query for user information\n\n"
            "\t Results will appear when you query.\n\n"
            "ABOUT US - You are here!\n\n"
            "EXIT BUTTON - close the app.\n"
        )
        howtoText.setWordWrap(True)
        howtoText.setObjectName("howtoText")

        content_layout.addWidget(howtoText)

        # ───── Developer Section ─────
        dev_Title = QLabel("{ Developers }")
        dev_Title.setObjectName("devTitle")

        dev_Text = QLabel(
            "This project was developed by a passionate team of\n"
            "computer science students who collaborated to create a\n"
            "simple and effective analysis tool.\n\n"
            "Each developer brought unique strengths to the project,\n"
            "from UI design to backend logic and overall user experience.\n\n"
            "We hope this tool makes exploring TikTok data easier\n"
            "and more fun for everyone!\n\n"
            "From us to you. Thank you for using this application!\n\n"
            "This app is optimised for use on FHD screen (1920x1080)\n\n"
        )
        dev_Text.setObjectName("devText")
        dev_Title.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(dev_Title)
        content_layout.addWidget(dev_Text)

        dev_form = QFormLayout()
        dev_form.setSpacing(10)

        def create_link(url):
            label = QLabel(f'<a href="{url}">{url}</a>')
            label.setOpenExternalLinks(True)
            label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            label.setCursor(QCursor(Qt.PointingHandCursor))
            return label

        dev_form.addRow("Elin Eunjung Park:", create_link("https://github.com/ElinEunjung"))
        dev_form.addRow("Ibrahim Khan:", create_link("https://github.com/DR4G0N101"))
        dev_form.addRow("Amalie Nilsen:", create_link("https://github.com/amalie246"))
        dev_form.addRow("Oda Nøstdahl:", create_link("https://github.com/Odanostdahl"))

        content_layout.addLayout(dev_form)

        # Connect content widget to scroll area
        scroll.setWidget(content_widget)

        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        # ───── Version ─────
        version_label = QLabel(f"Version: v{__version__}")
        version_label.setObjectName("versionLabel")

        # ───── Copyright ─────
        copyright_label = QLabel("© 2025 PEATA. All rights reserved.")
        copyright_label.setObjectName("copyrightLabel")

        # ───── Layout for version + copyright ─────
        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(0)
        footer_layout.setContentsMargins(0, 20, 0, 10)

        footer_container = QWidget()
        footer_inner_layout = QVBoxLayout(footer_container)
        footer_inner_layout.setSpacing(2)
        footer_inner_layout.setAlignment(Qt.AlignCenter)

        footer_inner_layout.addWidget(version_label, alignment=Qt.AlignCenter)
        footer_inner_layout.addWidget(copyright_label, alignment=Qt.AlignCenter)

        footer_layout.addWidget(footer_container)
        content_layout.addLayout(footer_layout)
