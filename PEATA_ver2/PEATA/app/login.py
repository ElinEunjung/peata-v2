import requests
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFormLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, Qt

class LoginWidget(QWidget):
    login_successful = pyqtSignal(str, str, str, str)  # client_id, client_key, client_secret, access_token

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login to TikTok API")
        self.access_token = None

        # ───── Layouts ─────
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # ───── Title ─────
        title = QLabel("Log in")
        title.setFont(QFont("Helvetica", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # ───── Input fields ─────
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Client ID")

        self.client_key_input = QLineEdit()
        self.client_key_input.setPlaceholderText("Client Key")

        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("Client Secret")
        self.client_secret_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Client ID:", self.client_id_input)
        form_layout.addRow("Client Key:", self.client_key_input)
        form_layout.addRow("Client Secret:", self.client_secret_input)

        main_layout.addLayout(form_layout)

        # ───── Login Button ─────
        login_btn = QPushButton("Log in")
        login_btn.setFont(QFont("Helvetica", 12, QFont.Bold))
        login_btn.clicked.connect(self.login)
        main_layout.addWidget(login_btn)

        self.setLayout(main_layout)

    def login(self):
        client_id = self.client_id_input.text().strip()
        client_key = self.client_key_input.text().strip()
        client_secret = self.client_secret_input.text().strip()

        if not client_id or not client_key or not client_secret:
            QMessageBox.warning(self, "Login Error", "All fields must be filled.")
            return

        # ───── Developer test login (bypass real API) ─────
        if client_id == "id" and client_key == "key" and client_secret == "secret":
            QMessageBox.information(self, "Developer Login", "Logged in with developer test credentials.")
            self.access_token = "developer_fake_access_token"
            self.login_successful.emit(client_id, client_key, client_secret, self.access_token)
            self.hide()
            return

        # ───── Normal API Login ─────
        success, message = self.test_connection(client_id, client_key, client_secret)

        if success:
            QMessageBox.information(self, "Success", message)
            self.login_successful.emit(client_id, client_key, client_secret, self.access_token)
            self.hide()
        else:
            QMessageBox.critical(self, "Failed", message)

    def test_connection(self, client_id, client_key, client_secret):
        endpoint = "https://open.tiktokapis.com/v2/oauth/token/"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'client_key': client_key,
            'grant_type': 'client_credentials'
        }

        try:
            response = requests.post(endpoint, headers=headers, data=data)
            if response.status_code == 200:
                try:
                    json_resp = response.json()
                    if "error" in json_resp:
                        return False, "Incorrect login parameters."
                    if "access_token" in json_resp:
                        self.access_token = json_resp['access_token']
                        return True, "Access token retrieved."
                    return False, "Unexpected server response."
                except ValueError:
                    return False, "Invalid JSON response."
            else:
                return False, f"Server error: {response.status_code} - {response.text}"

        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"
