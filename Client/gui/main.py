# Client/gui/main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt

from gui.views.welcome import WelcomeScreen
from gui.views.terms import TermsScreen
from gui.views.login import LoginScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RaceTech Client")
        self.setFixedSize(520, 500)
        self.setStyleSheet("font-family: Segoe UI; background-color: white;")

        self.agreed_to_terms = False
        self.racetech_token = None

        # סטאק מסכים
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # יצירת המסכים
        self.welcome_screen = WelcomeScreen(self.go_to_terms)
        print("[DEBUG] Creating TermsScreen with terms_agreed_handler as on_continue")
        self.terms_screen = TermsScreen(self.terms_agreed_handler)
        self.login_screen = LoginScreen(self.finish_login_with_token)

        self.stack.addWidget(self.welcome_screen)  # index 0
        self.stack.addWidget(self.terms_screen)    # index 1
        self.stack.addWidget(self.login_screen)    # index 2

        self.stack.setCurrentIndex(0)

    def go_to_terms(self):
        print("[DEBUG] go_to_terms called")
        self.stack.setCurrentIndex(1)

    def terms_agreed_handler(self):
        print("[DEBUG] terms_agreed_handler called")
        self.agreed_to_terms = True
        self.stack.setCurrentIndex(2)

    def go_to_login(self):
        print("[DEBUG] go_to_login called")
        if self.agreed_to_terms:
            self.stack.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Terms Not Accepted", "Please accept the terms before logging in.")

    def finish_login_with_token(self, token=None):
        print("[DEBUG] finish_login_with_token called")
        self.racetech_token = token
        self.close()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    # Return the token after GUI closes
    return window.racetech_token

if __name__ == "__main__":
    main()
#             QCheckBox::indicator {