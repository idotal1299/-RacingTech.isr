# Client/gui/views/login.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from auth.token_service import get_valid_racetech_token
from utils.logger import log

class LoginScreen(QWidget):
    def __init__(self, on_success=None):
        super().__init__()
        self.on_success = on_success
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 60, 40, 40)

        title = QLabel("Login with Google")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("We use your Google account to verify your RaceTech identity.")
        desc.setFont(QFont("Segoe UI", 11))
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # כפתור התחברות
        login_btn = QPushButton("Sign in with Google")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4285F4;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3367D6;
            }
        """)
        login_btn.clicked.connect(self.login_with_google)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def login_with_google(self):
        print("[DEBUG] login_with_google called")
        try:
            token = get_valid_racetech_token()
            print(f"[DEBUG] got token: {token}")
            log(f"[LOGIN] Token: {token}")
            QMessageBox.information(self, "Login Successful", "You're now logged in!")
            if self.on_success:
                print("[DEBUG] calling on_success with token")
                self.on_success(token)
        except Exception as e:
            log(f"[LOGIN ERROR] {e}")
            print(f"[DEBUG] login error: {e}")
            QMessageBox.critical(self, "Login Failed", str(e))
