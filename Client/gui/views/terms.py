# Client/gui/views/terms.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QCheckBox,
    QMessageBox, QSpacerItem, QSizePolicy, QHBoxLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import os
import subprocess
import sys

def open_file(filepath):
    if sys.platform == "win32":
        os.startfile(filepath)
    elif sys.platform == "darwin":
        subprocess.call(("open", filepath))
    else:
        subprocess.call(("xdg-open", filepath))

class TermsScreen(QWidget):
    def __init__(self, on_continue):
        print("[DEBUG] TermsScreen __init__ called")
        super().__init__()
        self.on_continue = on_continue
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Before we begin...")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # קבצי טקסט
        terms_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/TermsOfUse.txt"))
        privacy_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/PrivacyPolicy.txt"))

        button_row = QHBoxLayout()

        terms_btn = QPushButton("View Terms of Use")
        terms_btn.setStyleSheet("background-color: transparent; color: #007ACC; text-decoration: underline;")
        terms_btn.clicked.connect(lambda: open_file(terms_path))

        privacy_btn = QPushButton("View Privacy Policy")
        privacy_btn.setStyleSheet("background-color: transparent; color: #007ACC; text-decoration: underline;")
        privacy_btn.clicked.connect(lambda: open_file(privacy_path))

        button_row.addWidget(terms_btn)
        button_row.addWidget(privacy_btn)
        layout.addLayout(button_row)

        # צ'קבוקס
        self.checkbox = QCheckBox("I agree to the Terms of Use and Privacy Policy")
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 10px;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 1px solid #555;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC;
                border: 1px solid #005999;
            }
        """)
        self.checkbox.stateChanged.connect(self.toggle_continue_button)
        layout.addWidget(self.checkbox)

        # כפתור המשך
        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setEnabled(False)
        self.continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """)
        self.continue_btn.clicked.connect(self.try_continue)
        print("[DEBUG] continue_btn clicked connected to try_continue")
        layout.addWidget(self.continue_btn)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def toggle_continue_button(self, state):
        print(f"[DEBUG] toggle_continue_button called, state={state}")
        self.continue_btn.setEnabled(state == Qt.Checked)

    def try_continue(self):
        print("[DEBUG] try_continue called")
        if self.checkbox.isChecked():
            print("[DEBUG] checkbox is checked, calling on_continue()")
            self.on_continue()
        else:
            print("[DEBUG] checkbox NOT checked")
            QMessageBox.warning(self, "Terms Not Accepted", "Please agree to the Terms of Use and Privacy Policy to continue.")
