import requests
import os
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                               QPushButton, QScrollArea, QGridLayout, QMessageBox, QFrame, QLineEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from db.movie_repo import MovieRepo
from views.showtime_view import ShowtimeView


class MainView(QMainWindow):
    def __init__(self, user_id=None, username=None, role="guest"):
        super().__init__()
        self.cache_dir = "posters_cache"
        if not os.path.exists(self.cache_dir): os.makedirs(self.cache_dir)

        self.user_id = user_id
        self.username = username if username else "Guest"
        self.role = role if role else "guest"
        self.movie_repo = MovieRepo()

        self.all_movie_data = []
        self.current_page_index = 0
        self.movies_per_page = 50

        self.setWindowTitle("Cinema World - IMDb Top 250")
        self.resize(1150, 850)

        container = QWidget()
        self.setCentralWidget(container)
        self.main_layout = QVBoxLayout(container)

        # Navbar
        navbar = QHBoxLayout()
        welcome_lbl = QLabel(f"🎬 Welcome, <b>{self.username}</b>")
        navbar.addWidget(welcome_lbl)
        navbar.addStretch()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search Movies...")
        self.search_bar.textChanged.connect(self.filter_movies)
        navbar.addWidget(self.search_bar)

        # Updated: Button text changes based on role
        self.btn_auth = QPushButton("Logout" if self.role != "guest" else "Login")
        self.btn_auth.clicked.connect(self.handle_auth_action)
        navbar.addWidget(self.btn_auth)
        self.main_layout.addLayout(navbar)

        # Grid / Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.movie_grid = QGridLayout(scroll_content)
        scroll.setWidget(scroll_content)
        self.main_layout.addWidget(scroll)

        pagination_layout = QHBoxLayout()
        self.btn_prev = QPushButton("Previous Page")
        self.btn_next = QPushButton("Next Page")
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.btn_prev)
        pagination_layout.addWidget(self.btn_next)
        self.main_layout.addLayout(pagination_layout)

        self.load_all_data()

    def load_all_data(self):
        self.all_movie_data = self.movie_repo.get_all_movies()[:250]
        self.update_page_display()

    def update_page_display(self):
        start = self.current_page_index * self.movies_per_page
        end = start + self.movies_per_page
        movies_to_show = self.all_movie_data[start:end]
        self.display_movies(movies_to_show, start_rank=start + 1)

    def display_movies(self, movies_to_show, start_rank):
        while self.movie_grid.count():
            child = self.movie_grid.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        for i, m in enumerate(movies_to_show):
            movie_id, title, _, duration, _, poster_url = m
            card = QFrame()
            card.setFixedWidth(160)
            card.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 6px;")
            layout = QVBoxLayout(card)

            img_lbl = QLabel()
            img_lbl.setFixedSize(140, 200)
            pix = self.get_cached_poster(movie_id, poster_url)
            if pix: img_lbl.setPixmap(pix.scaled(140, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            title_lbl = QLabel(title)
            title_lbl.setStyleSheet("font-weight: bold; font-size: 11px;")

            btn = QPushButton("Book Now")
            btn.clicked.connect(lambda checked, mid=movie_id, mt=title: self.book_movie(mid, mt))

            layout.addWidget(img_lbl);
            layout.addWidget(title_lbl);
            layout.addWidget(btn)
            self.movie_grid.addWidget(card, i // 6, i % 6)

    def get_cached_poster(self, movie_id, url):
        cache_path = os.path.join(self.cache_dir, f"movie_{movie_id}.jpg")
        if os.path.exists(cache_path): return QPixmap(cache_path)
        try:
            res = requests.get(url, timeout=3)
            with open(cache_path, 'wb') as f:
                f.write(res.content)
            return QPixmap(cache_path)
        except:
            return None

    def book_movie(self, mid, mt):
        self.sw = ShowtimeView(mid, mt, self.user_id, self.username, self.role)
        self.sw.show()

    def next_page(self):
        self.current_page_index += 1; self.update_page_display()

    def prev_page(self):
        self.current_page_index -= 1; self.update_page_display()

    def filter_movies(self):
        text = self.search_bar.text().lower()
        filtered = [m for m in self.all_movie_data if text in m[1].lower()]
        self.display_movies(filtered, 1)

    def handle_auth_action(self):
        """Unified login/logout handler."""
        if self.role == "guest":
            from views.login_window import LoginWindow
            self.login_win = LoginWindow()
            self.login_win.show()
        else:
            from views.start_window import StartWindow
            self.start = StartWindow()
            self.start.show()
        self.close()