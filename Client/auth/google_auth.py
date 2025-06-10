# Client/auth/google_auth.py

import os
import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox,
    QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from auth.token_service import get_valid_racetech_token
from utils.logger import log

def open_file(filepath):
    if sys.platform == "win32":
        os.startfile(filepath)
    elif sys.platform == "darwin":
        subprocess.call(("open", filepath))
    else:
        subprocess.call(("xdg-open", filepath))

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RaceTech Client")
        self.setFixedSize(520, 480)
        self.setStyleSheet("""
            QWidget {
                background-color: #f2f2f2;
            }
            QPushButton {
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
            }
            QLabel {
                font-size: 10pt;
            }
            QCheckBox {
                font-size: 12pt;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(40, 30, 40, 30)

        # לוגו
        logo_path = os.path.join(os.path.dirname(__file__), "../assets/logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo = QLabel()
            logo.setPixmap(pixmap)
            logo.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo)

        # כותרת
        title = QLabel("Welcome to RaceTech")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # תנאים ופרטיות
        terms_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/TermsOfUse.txt"))
        privacy_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/PrivacyPolicy.txt"))

        terms_button = QPushButton("View Terms of Use")
        terms_button.setStyleSheet("background-color: transparent; color: #007ACC; font-size: 12px; text-decoration: underline;")
        terms_button.setCursor(Qt.PointingHandCursor)
        terms_button.clicked.connect(lambda: open_file(terms_path))
        layout.addWidget(terms_button)

        privacy_button = QPushButton("View Privacy Policy")
        privacy_button.setStyleSheet("background-color: transparent; color: #007ACC; font-size: 12px; text-decoration: underline;")
        privacy_button.setCursor(Qt.PointingHandCursor)
        privacy_button.clicked.connect(lambda: open_file(privacy_path))
        layout.addWidget(privacy_button)

        # Checkbox
        self.accept_checkbox = QCheckBox("I accept the Terms of Use and Privacy Policy")
        self.accept_checkbox.stateChanged.connect(self.checkbox_changed)
        layout.addWidget(self.accept_checkbox)

        # כפתור התחברות
        self.login_button = QPushButton("Login with Google")
        self.login_button.setStyleSheet("""
            background-color: #4285F4;
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        self.login_button.setMinimumHeight(50)
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def checkbox_changed(self, state):
        self.login_button.setEnabled(state == Qt.Checked)

    def handle_login(self):
        if not self.accept_checkbox.isChecked():
            QMessageBox.warning(self, "Agreement Required", "You must accept the Terms of Use and Privacy Policy to continue.")
            return

        try:
            token = get_valid_racetech_token()
            QMessageBox.information(self, "Login Successful", "Logged in successfully!")
            log(f"RaceTech token: {token}")
            # המשך עבודה עם הטוקן
        except Exception as e:
            QMessageBox.critical(self, "Login Failed", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
