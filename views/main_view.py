from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget,
                               QPushButton, QListWidget, QListWidgetItem, QMessageBox)
from db.movie_repo import MovieRepo
from views.start_window import StartWindow
from db.connection import get_db_connection


class MainView(QMainWindow):
    def __init__(self, username, role):
        super().__init__()
        self.setWindowTitle(f"Cinema App - {role.capitalize()} Panel")
        self.setFixedSize(600, 500)

        self.username = username
        self.role = role
        self.movie_repo = MovieRepo()

        layout = QVBoxLayout()

        # Header
        self.label = QLabel(f"Welcome, {username}!")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label)

        # Content based on Role
        if role == 'admin':
            layout.addWidget(QLabel("ADMIN CONSOLE"))
            self.btn_clear_bookings = QPushButton("Clear All Bookings (Maintenance)")
            self.btn_clear_bookings.setStyleSheet("background-color: #c0392b; color: white;")
            self.btn_clear_bookings.clicked.connect(self.admin_clear_data)  # This was the error!
            layout.addWidget(self.btn_clear_bookings)
        else:
            layout.addWidget(QLabel("Available Movies:"))
            self.movie_list = QListWidget()
            self.load_movies()
            layout.addWidget(self.movie_list)

            self.btn_book = QPushButton("Book Selected")
            self.btn_book.clicked.connect(self.book_movie)
            layout.addWidget(self.btn_book)

        # Logout Button
        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_movies(self):
        movies = self.movie_repo.get_all_movies()
        for m in movies:
            # m = (id, title, genre, duration, description)
            item_text = f"{m[1]} ({m[2]}) - {m[3]} min"
            item = QListWidgetItem(item_text)
            item.setData(1, m[0])  # Store the hidden ID
            self.movie_list.addItem(item)

    def book_movie(self):
        selected = self.movie_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a movie first!")
            return

        movie_id = selected.data(1)
        movie_name = selected.text()

        # Fix: ensure this matches your filename
        try:
            from views.showtime_view import ShowtimeView
            self.showtime_window = ShowtimeView(movie_id, movie_name)
            self.showtime_window.show()
        except ModuleNotFoundError:
            # If the folder 'views' is already the current package, try this:
            from showtime_view import ShowtimeView
            self.showtime_window = ShowtimeView(movie_id, movie_name)
            self.showtime_window.show()

    def admin_clear_data(self):
        # This function must be inside the MainView class!
        reply = QMessageBox.question(self, "Confirm", "Are you sure you want to clear all bookings?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM booked_seats; DELETE FROM bookings;")
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Admin", "All bookings have been cleared!")

    def logout(self):
        self.start = StartWindow()
        self.start.show()
        self.close()