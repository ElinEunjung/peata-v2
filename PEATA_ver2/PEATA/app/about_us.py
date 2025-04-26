from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

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
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        title_text = QLabel(
            "Platform Engagement Analysis and Tracking Application or PEATA is\n"
            "is a lightweight desktop tool designed to help users\n"
            "explore and analyze public data from social media platforms like TikTok.\n\n"

            "With a clean interface and customizable search options,\n"
            "PEATA makes it easy to query and view information about\n"
            "users, videos, and comments.\n\n"
            
            "Whether you're a researcher, a marketer, or just curious,\n"
            "PEATA helps you gather insights quickly and efficiently.\n\n"
            )
        title_text.setStyleSheet("font-size: 22px;")
        # title_text.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(title)
        content_layout.addWidget(title_text)

        # ───── How to Use ─────
        howtoTitle = QLabel("{ How to Use This App }")
        howtoTitle.setStyleSheet("font-size: 32px; font-weight: bold;")
        howtoTitle.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(howtoTitle)

        instructions = QLabel(
            "🖱️ Click 'Video Query', 'Comment Query', or 'User Query' from the left.\n\n"
            "✍️ Fill in filters like date, region, keywords.\n\n"
            "▶️ Press 'Run Query' to execute.\n\n"
            "📋 Results will appear (future feature).\n\n"
            "ℹ️ About Us for more info.\n\n"
            "❌ Exit button to close the app."
            
        )
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignLeft)
        instructions.setStyleSheet("font-size: 16px;")

        content_layout.addWidget(instructions)

        # ───── Developer Section ─────
        devTitle = QLabel("{ Developers }")
        devTitle.setStyleSheet("font-size: 32px; font-weight: bold;")
        devTitle.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(devTitle)

        dev_form = QFormLayout()
        dev_form.setSpacing(10)

        def create_link(url):
            label = QLabel(f'<a href="{url}">{url}</a>')
            label.setOpenExternalLinks(True)
            label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            label.setCursor(QCursor(Qt.PointingHandCursor))
            return label

        dev_form.addRow("Ibrahim Khan:", create_link("https://github.com/DR4G0N101"))
        dev_form.addRow("Elin Eunjung Park:", create_link("https://github.com/ElinEunjung"))
        dev_form.addRow("Oda Nøstdahl:", create_link("https://github.com/Odanostdahl"))
        dev_form.addRow("Amalie Nilsen:", create_link("https://github.com/amalie246"))

        content_layout.addLayout(dev_form)

        # Connect content widget to scroll area
        scroll.setWidget(content_widget)

        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
