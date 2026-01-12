from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from services.auth_service import AuthService


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 350)

        self.auth_service = AuthService()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(15)
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel("Welcome Back")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Log In")
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_button)

        self.back_button = QPushButton("Go Back")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setStyleSheet("background-color: transparent; color: #bdc3c7; border: 1px solid #555;")
        self.layout.addWidget(self.back_button)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Warning", "Please fill in all fields!")
            return

        # 1. Attempt login
        if self.auth_service.login(username, password):
            # 2. Get the user data that was just saved in memory
            user_data = self.auth_service.current_user
            # user_data is a tuple: (id, username, password, role, first_name, last_name)
            role = user_data[3]

            QMessageBox.information(self, "Success", f"Welcome back, {username}!")

            # 3. Open the main window and pass the role
            from views.main_view import MainView
            self.main_window = MainView(username, role)
            self.main_window.show()

            # 4. Close the login window
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password")

    def go_back(self):
        from views.start_window import StartWindow
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()