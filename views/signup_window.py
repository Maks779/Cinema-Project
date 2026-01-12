from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from services.auth_service import AuthService

class SignupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setFixedSize(400, 450)

        self.auth_service = AuthService()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        central_widget.setLayout(layout)

        title = QLabel("Create Account")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("First Name")
        layout.addWidget(self.name_input)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Last Name")
        layout.addWidget(self.surname_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.btn_register = QPushButton("Create Account")
        self.btn_register.setMinimumHeight(45)
        self.btn_register.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.btn_register.clicked.connect(self.handle_register)
        layout.addWidget(self.btn_register)

        self.btn_back = QPushButton("Go Back")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setStyleSheet("background-color: transparent; color: #bdc3c7; border: 1px solid #555;")
        layout.addWidget(self.btn_back)

    def handle_register(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not all([name, surname, username, password]):
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        if self.auth_service.register(name, surname, username, password):
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.go_back()
        else:
            QMessageBox.critical(self, "Error", "Failed to create account.")

    def go_back(self):
        from views.start_window import StartWindow
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()