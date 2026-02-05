from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from views.login_window import LoginWindow
from views.signup_window import SignupWindow

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinema Booking - Welcome")
        self.setFixedSize(400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        central_widget.setLayout(layout)

        title = QLabel("Welcome to Cinema World")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.btn_login = QPushButton("Log In")
        self.btn_login.setMinimumHeight(50)
        self.btn_login.clicked.connect(self.open_login)
        layout.addWidget(self.btn_login)

        self.btn_signup = QPushButton("Sign Up")
        self.btn_signup.setMinimumHeight(50)
        self.btn_signup.clicked.connect(self.open_signup)
        layout.addWidget(self.btn_signup)

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_signup(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()