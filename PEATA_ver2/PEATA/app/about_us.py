from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

class AboutUs(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(30)

        # ───── Title and Message ─────
        title = QLabel("{ About This App }")
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        thank_you = QLabel("Thank you for using this application!")
        thank_you.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)
        main_layout.addWidget(thank_you)

        # ───── Developer List ─────
        devTitle = QLabel("{ Developers }")
        devTitle.setStyleSheet("font-size: 32px; font-weight: bold;")
        devTitle.setAlignment(Qt.AlignCenter)
        
        main_layout.addWidget(devTitle)

        dev_form = QFormLayout()
        dev_form.setSpacing(10)

        def create_link(url):
            label = QLabel(f'<a href="{url}">{url}</a>')
            label.setOpenExternalLinks(True)
            label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            label.setCursor(QCursor(Qt.PointingHandCursor))
            return label

        dev_form.addRow("Ibrahim Khan:\t", create_link("https://github.com/DR4G0N101"))
        dev_form.addRow("Elin Eunjung Park:\t", create_link("https://github.com/ElinEunjung"))
        dev_form.addRow("Oda Nøstdahl:\t", create_link("https://github.com/Odanostdahl"))
        dev_form.addRow("Amalie Nilsen:\t", create_link("https://github.com/amalie246"))

        main_layout.addLayout(dev_form)

        self.setLayout(main_layout)
