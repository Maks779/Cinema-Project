from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QIcon
import os

from ui.styles import apply_style


def fade_to_window(current: QWidget, next_cls, *args, **kwargs):
    """
    Простий fade-перехід між вікнами.
    Не чіпає логіку вікон, тільки показ/закриття.
    """
    next_win = next_cls(*args, **kwargs)
    # Синхронізуємо геометрію, щоб не було стрибка
    next_win.setGeometry(current.geometry())
    next_win.setWindowOpacity(0.0)
    next_win.show()

    anim_out = QPropertyAnimation(current, b"windowOpacity")
    anim_out.setDuration(300)
    anim_out.setStartValue(1.0)
    anim_out.setEndValue(0.0)
    anim_out.setEasingCurve(QEasingCurve.InOutQuad)

    anim_in = QPropertyAnimation(next_win, b"windowOpacity")
    anim_in.setDuration(300)
    anim_in.setStartValue(0.0)
    anim_in.setEndValue(1.0)
    anim_in.setEasingCurve(QEasingCurve.InOutQuad)

    def close_current():
        current.close()

    anim_out.finished.connect(close_current)

    anim_out.start()
    anim_in.start()

    return next_win


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log in - CineBooking")

        self.set_window_icon()
        self.auth_service = None

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
        card.setFixedSize(520, 620)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 45, 50, 45)
        card_layout.setSpacing(0)

        logo_path = "assets/cinema_logo.png"
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_label.setObjectName("logoInCard")
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(
                logo_pixmap.scaledToHeight(50, Qt.SmoothTransformation)
            )
            logo_label.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(logo_label)

        card_layout.addSpacing(15)

        title = QLabel("Welcome back")
        title.setObjectName("authTitle")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        card_layout.addSpacing(8)

        subtitle = QLabel("Log in to manage your bookings")
        subtitle.setObjectName("authSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(25)

        lbl_user = QLabel("Username")
        lbl_user.setObjectName("fieldLabel")
        card_layout.addWidget(lbl_user)

        card_layout.addSpacing(6)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.textChanged.connect(lambda: self.clear_error("username"))
        card_layout.addWidget(self.username_input)

        self.error_labels["username"] = QLabel()
        self.error_labels["username"].setObjectName("errorLabel")
        self.error_labels["username"].hide()
        card_layout.addWidget(self.error_labels["username"])

        card_layout.addSpacing(15)

        lbl_pass = QLabel("Password")
        lbl_pass.setObjectName("fieldLabel")
        card_layout.addWidget(lbl_pass)

        card_layout.addSpacing(6)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.textChanged.connect(lambda: self.clear_error("password"))
        card_layout.addWidget(self.password_input)

        self.error_labels["password"] = QLabel()
        self.error_labels["password"].setObjectName("errorLabel")
        self.error_labels["password"].hide()
        card_layout.addWidget(self.error_labels["password"])

        card_layout.addSpacing(25)

        btn_login = QPushButton("Log in")
        btn_login.setObjectName("submitButton")
        btn_login.clicked.connect(self.handle_login)
        card_layout.addWidget(btn_login)

        card_layout.addSpacing(12)

        btn_back = QPushButton("Back to start")
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
        if field == "username":
            self.username_input.setProperty("error", True)
            self.username_input.setStyleSheet(
                """
                QLineEdit[error="true"] {
                    border: 2px solid #e74c3c !important;
                    background: rgba(231, 76, 60, 0.1);
                }
            """
            )
        elif field == "password":
            self.password_input.setProperty("error", True)
            self.password_input.setStyleSheet(
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
        if field == "username":
            self.username_input.setProperty("error", False)
            self.username_input.setStyleSheet("")
        elif field == "password":
            self.password_input.setProperty("error", False)
            self.password_input.setStyleSheet("")

        if field in self.error_labels:
            self.error_labels[field].hide()

    def handle_login(self):
        from services.auth_service import AuthService

        self.clear_error("username")
        self.clear_error("password")

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        has_error = False

        if not username:
            self.show_error("username", "Please enter your username")
            has_error = True

        if not password:
            self.show_error("password", "Please enter your password")
            has_error = True

        if has_error:
            return

        if self.auth_service is None:
            self.auth_service = AuthService()

        if self.auth_service.login(username, password):
            user_data = self.auth_service.current_user
            
            user_id = user_data[0]
            username = user_data[1]
            role = user_data[5]

            if role == "admin":
                from views.admin_panel import AdminPanel

                self.next_window = AdminPanel(username)
            else:
                from views.main_view import MainView

                self.next_window = MainView(user_id=user_id, username=username, role=role)

            self.next_window.showMaximized()
            self.close()
        else:
            self.show_error("username", "Invalid username or password")
            self.show_error("password", "Invalid username or password")

    def go_back(self):
        from views.start_window import StartWindow

        self.start_window = StartWindow()
        self.start_window.show()
        self.close()
