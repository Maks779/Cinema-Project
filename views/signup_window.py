from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
import os
import traceback

from ui.styles import apply_style
from db.user_repo import UserRepo
from utils.validators import PasswordValidator, UsernameValidator, NameValidator


class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign up - CineBooking")

        self.set_window_icon()
        self.user_repo = UserRepo()

        self.error_labels = {}
        self.bg_label = None      # NEW
        self.overlay = None       # NEW

        self.init_ui()
        apply_style(self, "auth")
        self.setWindowState(Qt.WindowMaximized)

    def set_window_icon(self):
        icon_path = "assets/cinema_logo.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def init_ui(self):
        # --- Головний контейнер ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- ШАР 1: фон ---
        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        bg_path = "assets/bg_photo2.png"
        if not os.path.exists(bg_path):
            bg_path = "assets/bg_photo.png"
        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path))
        else:
            self.bg_label.setStyleSheet("background-color: #000000;")

        # --- ШАР 2: затемнюючий overlay ---
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.75);")

        # --- ШАР 3: існуючий контент (НЕ змінюємо верстку) ---
        main_layout.addStretch(1)

        h_layout = QHBoxLayout()
        h_layout.addStretch(1)

        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedSize(520, 800)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 35, 50, 35)
        card_layout.setSpacing(0)

        logo_path = "assets/cinema_logo.png"
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_label.setObjectName("logoInCard")
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(
                logo_pixmap.scaledToHeight(45, Qt.SmoothTransformation)
            )
            logo_label.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(logo_label)

        card_layout.addSpacing(12)

        title = QLabel("Create account")
        title.setObjectName("authTitle")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(6)

        subtitle = QLabel("Join CineBooking and never miss a movie")
        subtitle.setObjectName("authSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(18)

        lbl_first = QLabel("First name")
        lbl_first.setObjectName("fieldLabel")
        card_layout.addWidget(lbl_first)
        card_layout.addSpacing(6)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Your first name")
        self.first_name_input.textChanged.connect(
            lambda: self.clear_error("first_name")
        )
        card_layout.addWidget(self.first_name_input)

        self.error_labels["first_name"] = QLabel()
        self.error_labels["first_name"].setObjectName("errorLabel")
        self.error_labels["first_name"].hide()
        card_layout.addWidget(self.error_labels["first_name"])

        card_layout.addSpacing(12)

        lbl_last = QLabel("Last name")
        lbl_last.setObjectName("fieldLabel")
        card_layout.addWidget(lbl_last)
        card_layout.addSpacing(6)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Your last name")
        self.last_name_input.textChanged.connect(lambda: self.clear_error("last_name"))
        card_layout.addWidget(self.last_name_input)

        self.error_labels["last_name"] = QLabel()
        self.error_labels["last_name"].setObjectName("errorLabel")
        self.error_labels["last_name"].hide()
        card_layout.addWidget(self.error_labels["last_name"])

        card_layout.addSpacing(12)

        lbl_user = QLabel("Username")
        lbl_user.setObjectName("fieldLabel")
        card_layout.addWidget(lbl_user)
        card_layout.addSpacing(6)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.textChanged.connect(lambda: self.clear_error("username"))
        card_layout.addWidget(self.username_input)

        self.error_labels["username"] = QLabel()
        self.error_labels["username"].setObjectName("errorLabel")
        self.error_labels["username"].hide()
        card_layout.addWidget(self.error_labels["username"])

        card_layout.addSpacing(12)

        lbl_pass = QLabel("Password")
        lbl_pass.setObjectName("fieldLabel")
        card_layout.addWidget(lbl_pass)
        card_layout.addSpacing(6)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Choose a password")
        self.password_input.textChanged.connect(lambda: self.clear_error("password"))
        card_layout.addWidget(self.password_input)

        self.error_labels["password"] = QLabel()
        self.error_labels["password"].setObjectName("errorLabel")
        self.error_labels["password"].hide()
        card_layout.addWidget(self.error_labels["password"])

        password_hint = QLabel("Min 8 characters, uppercase, lowercase, number")
        password_hint.setObjectName("passwordHint")
        card_layout.addWidget(password_hint)

        card_layout.addSpacing(20)

        btn_signup = QPushButton("Create account")
        btn_signup.setObjectName("submitButton")
        btn_signup.clicked.connect(self.handle_signup)
        card_layout.addWidget(btn_signup)

        card_layout.addSpacing(12)

        btn_back = QPushButton("Back to login")
        btn_back.setObjectName("backButton")
        btn_back.clicked.connect(self.go_back)
        card_layout.addWidget(btn_back)

        h_layout.addWidget(card)
        h_layout.addStretch(1)

        main_layout.addLayout(h_layout)
        main_layout.addStretch(1)

    # NEW: розтягуємо фон і overlay
    def resizeEvent(self, event):
        if self.bg_label and self.overlay:
            size = self.size()
            self.bg_label.setGeometry(0, 0, size.width(), size.height())
            self.overlay.setGeometry(0, 0, size.width(), size.height())
        super().resizeEvent(event)

    def show_error(self, field, message):
        input_field = None

        if field == "first_name":
            input_field = self.first_name_input
        elif field == "last_name":
            input_field = self.last_name_input
        elif field == "username":
            input_field = self.username_input
        elif field == "password":
            input_field = self.password_input

        if input_field:
            input_field.setProperty("error", True)
            input_field.setStyleSheet(
                """
                QLineEdit[error="true"] {
                    border: 2px solid #e74c3c !important;
                    background: rgba(231, 76, 60, 0.1);
                }
            """
            )

        if field in self.error_labels:
            self.error_labels[field].setText(message)
            self.error_labels[field].show()

    def clear_error(self, field):
        input_field = None

        if field == "first_name":
            input_field = self.first_name_input
        elif field == "last_name":
            input_field = self.last_name_input
        elif field == "username":
            input_field = self.username_input
        elif field == "password":
            input_field = self.password_input

        if input_field:
            input_field.setProperty("error", False)
            input_field.setStyleSheet("")

        if field in self.error_labels:
            self.error_labels[field].hide()

    def handle_signup(self):
        try:
            print("🔵 handle_signup called")

            for field in ["first_name", "last_name", "username", "password"]:
                self.clear_error(field)

            first_name = self.first_name_input.text().strip()
            last_name = self.last_name_input.text().strip()
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()

            print(
                f"📝 Data: {username}, {first_name}, {last_name}, pwd_len={len(password)}"
            )

            has_error = False

            is_valid, error_msg = NameValidator.validate(first_name, "First name")
            if not is_valid:
                print(f"❌ First name error: {error_msg}")
                self.show_error("first_name", error_msg)
                has_error = True

            is_valid, error_msg = NameValidator.validate(last_name, "Last name")
            if not is_valid:
                print(f"❌ Last name error: {error_msg}")
                self.show_error("last_name", error_msg)
                has_error = True

            is_valid, error_msg = UsernameValidator.validate(username)
            if not is_valid:
                print(f"❌ Username error: {error_msg}")
                self.show_error("username", error_msg)
                has_error = True

            is_valid, error_msg = PasswordValidator.validate(password)
            if not is_valid:
                print(f"❌ Password error: {error_msg}")
                self.show_error("password", error_msg)
                has_error = True

            if has_error:
                print("⚠️ Validation failed, stopping")
                return

            print("✅ Validation passed, creating user...")

            success = self.user_repo.create_user(
                username, password, first_name, last_name
            )

            print(f"📊 Database result: {success}")

            if success:
                QMessageBox.information(
                    self, "Success", "Account created! You can now log in."
                )
                from views.login_window import LoginWindow

                self.login_window = LoginWindow()
                self.login_window.show()
                self.close()
            else:
                print("❌ Username already exists")
                self.show_error("username", "Username already exists")

        except Exception as e:
            print(f"💥 CRASH in handle_signup:")
            traceback.print_exc()
            QMessageBox.critical(
                self, "Error", f"An error occurred during registration:\n{str(e)}"
            )

    def go_back(self):
        from views.login_window import LoginWindow

        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
