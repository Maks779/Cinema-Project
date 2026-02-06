import os
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer

from ui.styles import apply_style
from ui.animations import slide_in_from_bottom


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineBooking")

        self.setMinimumSize(1024, 768)

        self.set_window_icon()

        self.bg_label = None
        self.overlay = None
        self.center_card = None
        self._first_show = True
        self._card_ready = False

        self.init_ui()
        apply_style(self, "start")

    def set_window_icon(self):
        icon_path = "assets/cinema_logo.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Фон
        self.bg_label = QLabel()
        self.bg_label.setObjectName("bgLabel")
        self.bg_label.setScaledContents(True)

        bg_path = "assets/bg_photo.png"
        if os.path.exists(bg_path):
            pix = QPixmap(bg_path)
            self.bg_label.setPixmap(pix)

        central_layout.addWidget(self.bg_label)

        self.overlay = QWidget(self.bg_label)
        self.overlay.setObjectName("overlay")

        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setContentsMargins(60, 50, 60, 50)
        overlay_layout.setSpacing(0)

        top_bar = QHBoxLayout()
        top_bar.setSpacing(15)

        logo_path = "assets/cinema_logo.png"
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_label.setObjectName("logoImage")
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(
                logo_pixmap.scaledToHeight(70, Qt.SmoothTransformation)
            )
            top_bar.addWidget(logo_label)

        title = QLabel("CINEBOOKING")
        title.setObjectName("appTitle")
        top_bar.addWidget(title)
        top_bar.addStretch()

        overlay_layout.addLayout(top_bar)
        overlay_layout.addStretch()

        # Center Card
        self.center_card = QFrame()
        self.center_card.setObjectName("centerCard")
        self.center_card.setFixedWidth(520)
        self.center_card.setVisible(False)

        card_layout = QVBoxLayout(self.center_card)
        card_layout.setContentsMargins(50, 50, 50, 50)
        card_layout.setSpacing(25)

        subtitle = QLabel("Book your next movie night")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)

        btn_login = QPushButton("Log in")
        btn_login.setObjectName("primaryButton")
        btn_login.clicked.connect(self.open_login)
        card_layout.addWidget(btn_login)

        btn_signup = QPushButton("Create account")
        btn_signup.setObjectName("secondaryButton")
        btn_signup.clicked.connect(self.open_signup)
        card_layout.addWidget(btn_signup)

        btn_guest = QPushButton("Continue as guest")
        btn_guest.setObjectName("ghostButton")
        btn_guest.clicked.connect(self.continue_as_guest)
        card_layout.addWidget(btn_guest)

        overlay_layout.addWidget(self.center_card, alignment=Qt.AlignCenter)
        overlay_layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)

        if self._first_show:
            self._first_show = False

            self.showNormal()

            QTimer.singleShot(10, lambda: self.setWindowState(Qt.WindowMaximized))

            QTimer.singleShot(50, self.update_overlay_geometry)

            QTimer.singleShot(150, self.show_card_with_animation)

    def show_card_with_animation(self):
        if self.center_card:
            self.center_card.setVisible(True)
            slide_in_from_bottom(self.center_card, duration=600)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_overlay_geometry()

    def update_overlay_geometry(self):
        if self.overlay and self.bg_label:
            self.overlay.setGeometry(self.bg_label.rect())

    def open_login(self):
        from views.login_window import LoginWindow

        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_signup(self):
        from views.signup_window import SignupWindow

        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()

    def continue_as_guest(self):
        from views.main_view import MainView

        self.main_view = MainView(username=None, role="guest")
        self.main_view.showMaximized()
        self.close()
