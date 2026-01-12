from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QListWidgetItem, \
    QMessageBox
from PySide6.QtCore import Qt
from db.connection import get_db_connection


class ShowtimeView(QMainWindow):
    def __init__(self, movie_id, movie_name):
        super().__init__()
        self.setWindowTitle("Select Showtime")
        self.setFixedSize(400, 400)
        self.movie_id = movie_id

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Showtimes for: {movie_name}"))

        self.showtime_list = QListWidget()
        self.load_showtimes()
        layout.addWidget(self.showtime_list)

        self.btn_next = QPushButton("Select Seats")
        self.btn_next.clicked.connect(self.open_seat_selection)
        layout.addWidget(self.btn_next)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_showtimes(self):
        conn = get_db_connection()
        if not conn: return
        cur = conn.cursor()
        # Fetch showtimes for this specific movie
        cur.execute("SELECT id, start_time, price FROM showtimes WHERE movie_id = %s", (self.movie_id,))
        for row in cur.fetchall():
            # row[1] is the start_time
            item = QListWidgetItem(f"Time: {row[1]} - Price: ${row[2]}")
            item.setData(Qt.UserRole, row[0])  # Store Showtime ID
            self.showtime_list.addItem(item)
        conn.close()

    def open_seat_selection(self):
        selected = self.showtime_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a time!")
            return

        showtime_id = selected.data(Qt.UserRole)

        # Try both import styles to be safe for your demo environment
        try:
            from views.seat_selection_view import SeatSelectionView
        except ModuleNotFoundError:
            from seat_selection_view import SeatSelectionView

        self.seat_window = SeatSelectionView(showtime_id)
        self.seat_window.show()
        self.close()