import requests
import os
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QFrame,
    QLineEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCursor, QIcon, QFontMetrics
from db.movie_repo import MovieRepo
from views.showtime_view import ShowtimeView


class MainView(QMainWindow):
    def __init__(self, user_id=None, username=None, role="guest"):
        super().__init__()
        self.cache_dir = "posters_cache"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.user_id = user_id
        self.username = username if username else "Guest"
        self.role = role if role else "guest"
        self.movie_repo = MovieRepo()

        self.all_movie_data = []
        self.current_page_index = 0
        self.movies_per_page = 50

        self.setWindowTitle("CineBooking - Browse Movies")

        icon_path = "assets/cinema_logo.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.bg_label = None
        self.overlay = None

        container = QWidget()
        self.setCentralWidget(container)

        self.setup_background(container)

        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.main_layout.setSpacing(20)

        navbar = QHBoxLayout()

        logo_label = QLabel()
        if os.path.exists(icon_path):
            logo_pix = QPixmap(icon_path)
            logo_label.setPixmap(
                logo_pix.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        logo_label.setFixedSize(40, 40)
        logo_label.setAlignment(Qt.AlignCenter)
        navbar.addWidget(logo_label)

        welcome_lbl = QLabel(
            f"Welcome, <span style='color: #ffb400;'>{self.username}</span>"
        )
        welcome_lbl.setStyleSheet(
            """
            QLabel {
                color: white; 
                font-size: 22px; 
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """
        )
        navbar.addWidget(welcome_lbl)

        navbar.addStretch()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for movies...")
        self.search_bar.setFixedWidth(400)
        self.search_bar.setStyleSheet(
            """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #ffb400;
                background-color: rgba(255, 255, 255, 0.15);
            }
        """
        )
        self.search_bar.textChanged.connect(self.filter_movies)
        navbar.addWidget(self.search_bar)

        navbar.addSpacing(20)

        self.btn_auth = QPushButton("Logout" if self.role != "guest" else "Login")
        self.btn_auth.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_auth.setStyleSheet(
            """
            QPushButton {
                background-color: #ffb400;
                color: #000000;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ffc947;
            }
            QPushButton:pressed {
                background-color: #e09e00;
            }
        """
        )
        self.btn_auth.clicked.connect(self.handle_auth_action)
        navbar.addWidget(self.btn_auth)

        self.main_layout.addLayout(navbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0,0,0,0.3);
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
        )

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")

        self.movie_grid = QGridLayout(scroll_content)
        self.movie_grid.setSpacing(25)
        self.movie_grid.setContentsMargins(10, 10, 10, 10)

        scroll.setWidget(scroll_content)
        self.main_layout.addWidget(scroll)

        pagination_layout = QHBoxLayout()
        self.btn_prev = QPushButton("← Previous")
        self.btn_next = QPushButton("Next →")

        pagination_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 10px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid #ffb400;
                color: #ffb400;
            }
            QPushButton:disabled {
                background-color: rgba(255, 255, 255, 0.05);
                color: #777;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """
        self.btn_prev.setStyleSheet(pagination_style)
        self.btn_next.setStyleSheet(pagination_style)
        self.btn_prev.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_next.setCursor(QCursor(Qt.PointingHandCursor))

        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next.clicked.connect(self.next_page)

        self.page_label = QLabel()
        self.page_label.setStyleSheet(
            "color: #ccc; font-size: 14px; font-weight: bold;"
        )

        pagination_layout.addStretch()
        self.btn_prev.setMinimumWidth(120)
        self.btn_next.setMinimumWidth(120)
        pagination_layout.addWidget(self.btn_prev)
        pagination_layout.addSpacing(15)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addSpacing(15)
        pagination_layout.addWidget(self.btn_next)
        pagination_layout.addStretch()

        self.main_layout.addLayout(pagination_layout)

        self.load_all_data()

    def setup_background(self, parent):
        self.bg_label = QLabel(parent)
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        bg_path = "assets/bg_photo3.png"
        if not os.path.exists(bg_path):
            bg_path = "assets/bg_photo2.png"
        if not os.path.exists(bg_path):
            bg_path = "assets/bg_photo.png"

        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path))
        else:
            self.bg_label.setStyleSheet("background-color: #1a1a1a;")

        self.overlay = QWidget(parent)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.85);")
        self.overlay.lower()

    def resizeEvent(self, event):
        if self.bg_label and self.overlay:
            size = self.centralWidget().size()
            self.bg_label.setGeometry(0, 0, size.width(), size.height())
            self.overlay.setGeometry(0, 0, size.width(), size.height())
        super().resizeEvent(event)

    def load_all_data(self):
        self.all_movie_data = self.movie_repo.get_all_movies()[:250]
        self.update_page_display()

    def update_page_display(self):
        total = len(self.all_movie_data)
        start = self.current_page_index * self.movies_per_page
        end = start + self.movies_per_page
        movies_to_show = self.all_movie_data[start:end]
        self.display_movies(movies_to_show, start_rank=start + 1)

        total_pages = max(1, (total + self.movies_per_page - 1) // self.movies_per_page)
        self.page_label.setText(f"Page {self.current_page_index + 1} / {total_pages}")

        self.btn_prev.setEnabled(self.current_page_index > 0)
        self.btn_next.setEnabled(end < total)

    def display_movies(self, movies_to_show, start_rank):
        while self.movie_grid.count():
            child = self.movie_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        columns = 5

        for i, m in enumerate(movies_to_show):
            movie_id = m[0]
            title = m[1]
            genre = m[2]
            description = m[4]
            poster_url = m[5]

            card = QFrame()
            card.setFixedSize(200, 420)
            card.setStyleSheet(
                """
                QFrame {
                    background-color: rgba(30, 30, 30, 0.7);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                }
                QFrame:hover {
                    background-color: rgba(50, 50, 50, 0.9);
                    border: 1px solid #ffb400;
                }
            """
            )

            layout = QVBoxLayout(card)
            layout.setContentsMargins(10, 10, 10, 15)
            layout.setSpacing(5)

            img_lbl = QLabel()
            img_lbl.setFixedSize(180, 260)
            img_lbl.setStyleSheet(
                "border-radius: 8px; border: none; background: transparent;"
            )
            img_lbl.setAlignment(Qt.AlignCenter)

            pix = self.get_cached_poster(movie_id, poster_url)
            if pix:
                img_lbl.setPixmap(
                    pix.scaled(180, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            else:
                img_lbl.setText("No Image")
                img_lbl.setStyleSheet(
                    "color: #777; font-size: 12px; border: 1px dashed #555;"
                )

            title_lbl = QLabel(title)
            title_lbl.setStyleSheet(
                """
                font-weight: bold; 
                font-size: 14px; 
                color: white; 
                background: transparent; 
                border: none;
            """
            )
            title_lbl.setWordWrap(True)
            title_lbl.setAlignment(Qt.AlignCenter)
            title_lbl.setFixedHeight(40)

            genre_lbl = QLabel(genre if genre else "Unknown Genre")
            genre_lbl.setStyleSheet(
                "color: #aaa; font-size: 11px; background: transparent; border: none;"
            )
            genre_lbl.setAlignment(Qt.AlignCenter)
            genre_lbl.setFixedHeight(15)

            desc_lbl = QLabel()
            desc_lbl.setStyleSheet(
                "color: #ccc; font-size: 11px; background: transparent; border: none;"
            )
            desc_lbl.setAlignment(Qt.AlignCenter)
            desc_lbl.setWordWrap(True)
            desc_lbl.setFixedHeight(35)

            full_description = (
                description if description else "No description available."
            )
            metrics = QFontMetrics(desc_lbl.font())
            elided_desc = metrics.elidedText(full_description, Qt.ElideRight, 180 * 2)
            desc_lbl.setText(elided_desc)

            btn = QPushButton("Book Now")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #ffb400;
                    color: black;
                    border: none;
                    border-radius: 15px;
                    padding: 5px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #ffc947;
                }
            """
            )
            btn.clicked.connect(
                lambda checked, mid=movie_id, mt=title, md=full_description: self.book_movie(
                    mid, mt, md
                )
            )

            layout.addWidget(img_lbl)
            layout.addWidget(title_lbl)
            layout.addWidget(genre_lbl)
            layout.addWidget(desc_lbl)
            layout.addWidget(btn)

            self.movie_grid.addWidget(card, i // columns, i % columns)

    def get_cached_poster(self, movie_id, url):
        cache_path = os.path.join(self.cache_dir, f"movie_{movie_id}.jpg")
        if os.path.exists(cache_path):
            return QPixmap(cache_path)
        try:
            res = requests.get(url, timeout=3)
            with open(cache_path, "wb") as f:
                f.write(res.content)
            return QPixmap(cache_path)
        except:
            return None

    def book_movie(self, mid, mt, md):
        self.sw = ShowtimeView(
            mid, mt, self.user_id, self.username, self.role, description=md
        )
        self.sw.showMaximized()
        self.close()

    def next_page(self):
        self.current_page_index += 1
        self.update_page_display()

    def prev_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.update_page_display()

    def filter_movies(self):
        text = self.search_bar.text().lower()
        filtered = [m for m in self.all_movie_data if text in m[1].lower()]
        self.display_movies(filtered, 1)

    def handle_auth_action(self):
        if self.role == "guest":
            from views.login_window import LoginWindow

            self.login_win = LoginWindow()
            self.login_win.show()
        else:
            from views.start_window import StartWindow

            self.start = StartWindow()
            self.start.show()
        self.close()
