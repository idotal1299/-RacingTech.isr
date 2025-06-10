# Client/gui/views/welcome.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
import os

class WelcomeScreen(QWidget):
    def __init__(self, on_continue):
        super().__init__()
        self.on_continue = on_continue
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 60, 40, 40)

        # לוגו
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/logo.png"))
        if os.path.exists(logo_path):
            logo = QLabel()
            pixmap = QPixmap(logo_path).scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            logo.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo)

        # טקסט כותרת
        title = QLabel("Welcome to RaceTech")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # טקסט משנה
        subtitle = QLabel("Your personal telemetry companion for iRacing.")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # כפתור המשך
        continue_btn = QPushButton("Start")
        continue_btn.setStyleSheet("""
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
        continue_btn.clicked.connect(self.on_continue)
        layout.addWidget(continue_btn)

        self.setLayout(layout)
