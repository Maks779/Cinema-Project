import requests
import os
from io import BytesIO
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                               QPushButton, QScrollArea, QGridLayout, QMessageBox, QFrame, QLineEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from db.movie_repo import MovieRepo
from db.connection import get_db_connection


class MainView(QMainWindow):
    def __init__(self, username=None, role="guest"):
        super().__init__()
        self.cache_dir = "posters_cache"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.username = username if username else "Guest"
        self.role = role if role else "guest"
        self.movie_repo = MovieRepo()
        self.all_movie_data = []

        self.setWindowTitle(f"Cinema App - {self.role.capitalize()} Panel")
        self.resize(1300, 850)  # Wider window to show off the new grid

        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QVBoxLayout(container)

        # --- NAVBAR ---
        navbar = QHBoxLayout()
        welcome_lbl = QLabel(f"🎬 Welcome, {self.username}!")
        welcome_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        navbar.addWidget(welcome_lbl)
        navbar.addStretch()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search...")
        self.search_bar.setFixedWidth(250)
        self.search_bar.setStyleSheet("padding: 6px; border-radius: 12px; border: 1px solid #ccc;")
        self.search_bar.textChanged.connect(self.filter_movies)
        navbar.addWidget(self.search_bar)

        btn_text = "Login / Register" if self.role == "guest" else "Logout"
        self.btn_auth = QPushButton(btn_text)
        self.btn_auth.setStyleSheet(
            "background-color: #3498db; color: white; padding: 6px 12px; border-radius: 5px; font-weight: bold;")
        self.btn_auth.clicked.connect(self.logout)
        navbar.addWidget(self.btn_auth)
        main_layout.addLayout(navbar)

        # --- MOVIE GRID ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.movie_grid = QGridLayout(scroll_content)
        self.movie_grid.setSpacing(10)  # Tighter spacing for smaller cards
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        self.load_movies_grid()

    def get_cached_poster(self, movie_id, url):
        cache_path = os.path.join(self.cache_dir, f"movie_{movie_id}.jpg")
        if os.path.exists(cache_path):
            return QPixmap(cache_path)
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                with open(cache_path, 'wb') as f:
                    f.write(res.content)
                return QPixmap(cache_path)
        except:
            pass
        return None

    def display_movies(self, movies_to_show):
        while self.movie_grid.count():
            child = self.movie_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        row, col = 0, 0
        for m in movies_to_show:
            movie_id, title, genre, duration, desc, poster_url = m

            card = QFrame()
            # 50% SMALLER: Width reduced to 140px
            card.setFixedWidth(145)
            card.setStyleSheet("background-color: white; border: 1px solid #dcdde1; border-radius: 8px; padding: 5px;")
            card_layout = QVBoxLayout(card)

            # Poster (Shrunk to 120x180)
            poster_label = QLabel()
            poster_label.setFixedSize(130, 180)
            poster_label.setAlignment(Qt.AlignCenter)
            poster_label.setStyleSheet("background-color: #f5f6fa; border: none;")

            pix = self.get_cached_poster(movie_id, poster_url)
            if pix and not pix.isNull():
                poster_label.setPixmap(pix.scaled(
                    poster_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation  # High resolution fix
                ))
            else:
                poster_label.setText("🎬")

            card_layout.addWidget(poster_label, alignment=Qt.AlignCenter)

            # Mini Title
            title_lbl = QLabel(f"<b>{title}</b>")
            title_lbl.setWordWrap(True)
            title_lbl.setStyleSheet("font-size: 11px;")
            title_lbl.setMinimumHeight(35)

            # Mini Info
            info_lbl = QLabel(f"{duration}m")
            info_lbl.setStyleSheet("color: #7f8c8d; font-size: 10px;")

            btn_book = QPushButton("Book")
            btn_book.setStyleSheet(
                "background-color: #27ae60; color: white; border-radius: 3px; font-size: 10px; font-weight: bold;")
            btn_book.clicked.connect(lambda checked, mid=movie_id, mt=title: self.book_movie(mid, mt))

            card_layout.addWidget(title_lbl)
            card_layout.addWidget(info_lbl)
            card_layout.addWidget(btn_book)

            self.movie_grid.addWidget(card, row, col)

            # FIT MORE MOVIES: Increased to 8 columns
            col += 1
            if col > 7:
                col = 0
                row += 1

    def load_movies_grid(self):
        self.all_movie_data = self.movie_repo.get_all_movies()
        self.display_movies(self.all_movie_data)

    def filter_movies(self):
        search_text = self.search_bar.text().lower()
        filtered = [m for m in self.all_movie_data if search_text in m[1].lower() or search_text in m[2].lower()]
        self.display_movies(filtered)

    def book_movie(self, mid, mt):
        if self.role == "guest":
            QMessageBox.warning(self, "Login Required", "Please log in to book!")
            self.logout()
            return
        from views.showtime_view import ShowtimeView
        self.sw = ShowtimeView(mid, mt)
        self.sw.show()

    def logout(self):
        from views.start_window import StartWindow
        self.start = StartWindow()
        self.start.show()
        self.close()