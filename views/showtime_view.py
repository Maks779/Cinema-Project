from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QPushButton, QComboBox, QMessageBox, QDateEdit)
from PySide6.QtGui import QTextCharFormat, QColor
from PySide6.QtCore import Qt, QDate
from db.connection import get_db_connection


class ShowtimeView(QWidget):
    def __init__(self, movie_id, movie_title, user_id=None, username="Guest", role="guest"):
        super().__init__()
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.user_id = user_id
        self.username = username
        self.role = role
        self.selected_seats = []
        self.showtimes_data = []

        self.setWindowTitle(f"Booking: {movie_title}")
        self.resize(850, 850)
        self.layout = QVBoxLayout(self)

        # --- Header ---
        header = QHBoxLayout()
        header.addWidget(QLabel(f"<b>Movie:</b> {movie_title}"))
        header.addStretch()

        header.addWidget(QLabel("Date:"))
        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setMinimumDate(QDate.currentDate())
        self.calendar = self.date_picker.calendarWidget()
        self.date_picker.dateChanged.connect(self.load_available_showtimes)
        header.addWidget(self.date_picker)

        header.addWidget(QLabel("Time:"))
        self.time_combo = QComboBox()
        self.time_combo.currentIndexChanged.connect(self.load_seats)
        header.addWidget(self.time_combo)
        self.layout.addLayout(header)

        # --- Screen Graphic ---
        screen_lbl = QLabel("SCREEN")
        screen_lbl.setStyleSheet("background-color: #333; color: white; border-radius: 5px; padding: 10px;")
        screen_lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(screen_lbl)

        # --- Seat Grid ---
        self.seat_container = QWidget()
        self.grid = QGridLayout(self.seat_container)
        self.layout.addWidget(self.seat_container)

        # --- Footer: Price and Confirm ---
        footer = QHBoxLayout()
        self.price_lbl = QLabel("Total: $0.00")
        self.price_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #2ecc71;")
        footer.addWidget(self.price_lbl)
        footer.addStretch()

        self.confirm_btn = QPushButton("Select Seats")
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.setMinimumWidth(200)
        self.confirm_btn.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; font-weight: bold; padding: 12px; border-radius: 5px; }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }
        """)
        self.confirm_btn.clicked.connect(self.process_booking)
        footer.addWidget(self.confirm_btn)
        self.layout.addLayout(footer)

        self.highlight_available_dates()
        self.load_available_showtimes()

    def highlight_available_dates(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT start_time::date FROM showtimes WHERE movie_id = %s", (self.movie_id,))
        dates = cur.fetchall()
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#2ecc71"))
        fmt.setForeground(Qt.white)
        for d_tuple in dates:
            self.calendar.setDateTextFormat(QDate(d_tuple[0].year, d_tuple[0].month, d_tuple[0].day), fmt)
        cur.close()
        conn.close()

    def load_available_showtimes(self):
        conn = get_db_connection()
        cur = conn.cursor()
        selected_date = self.date_picker.date().toPython()
        self.showtimes_data = []
        self.time_combo.clear()

        cur.execute("""
            SELECT id, room_id, start_time, price FROM showtimes 
            WHERE movie_id = %s AND start_time::date = %s
            ORDER BY start_time ASC
        """, (self.movie_id, selected_date))

        self.showtimes_data = cur.fetchall()
        if not self.showtimes_data:
            self.time_combo.addItem("No screenings")
            self.time_combo.setEnabled(False)
        else:
            self.time_combo.setEnabled(True)
            for sid, rid, st, pr in self.showtimes_data:
                self.time_combo.addItem(f"Room {rid} @ {st.strftime('%H:%M')} (${pr:.2f})")
        cur.close()
        conn.close()

    def load_seats(self):
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        self.selected_seats = []
        self.update_ui()

        idx = self.time_combo.currentIndex()
        if not self.showtimes_data or idx < 0: return

        showtime_id = self.showtimes_data[idx][0]

        conn = get_db_connection()
        cur = conn.cursor()
        # This query checks the database for seats that are already sold
        cur.execute("SELECT seat_id FROM bookings WHERE showtime_id = %s", (showtime_id,))
        taken_seats = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()

        for r in range(8):
            for c in range(10):
                seat_id = f"{chr(65 + r)}{c + 1}"
                btn = QPushButton(seat_id)
                btn.setFixedSize(45, 45)
                # If seat is in DB, make it Red (Taken)
                if seat_id in taken_seats:
                    btn.setEnabled(False)
                    btn.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 5px;")
                else:
                    btn.setCheckable(True)
                    btn.setStyleSheet("QPushButton { background-color: #2ecc71; color: white; border-radius: 5px; }"
                                      "QPushButton:checked { background-color: #f39c12; }")
                    btn.clicked.connect(lambda checked, s=seat_id: self.toggle_seat(s))
                self.grid.addWidget(btn, r, c)

    def toggle_seat(self, s):
        if s in self.selected_seats:
            self.selected_seats.remove(s)
        else:
            self.selected_seats.append(s)
        self.update_ui()

    def update_ui(self):
        """Calculates total price and updates the button state."""
        count = len(self.selected_seats)
        idx = self.time_combo.currentIndex()

        if idx >= 0 and self.showtimes_data:
            price_per_seat = float(self.showtimes_data[idx][3])
            total = count * price_per_seat
            self.price_lbl.setText(f"Total: ${total:.2f}")
        else:
            self.price_lbl.setText("Total: $0.00")

        self.confirm_btn.setText(f"Confirm {count} Seats" if count > 0 else "Select Seats")
        self.confirm_btn.setEnabled(count > 0)

    def process_booking(self):
        if self.role == "guest":
            QMessageBox.information(self, "Login Required", "Please login to complete booking.")
            from views.login_window import LoginWindow
            self.lw = LoginWindow()
            self.lw.show()
            self.close()
            return

        conn = get_db_connection()
        cur = conn.cursor()
        showtime_id = self.showtimes_data[self.time_combo.currentIndex()][0]
        try:
            # Permanently save each seat to the DB
            for seat in self.selected_seats:
                cur.execute("INSERT INTO bookings (user_id, showtime_id, seat_id) VALUES (%s, %s, %s)",
                            (self.user_id, showtime_id, seat))
            conn.commit()
            QMessageBox.information(self, "Success", f"Booked {len(self.selected_seats)} tickets!")
            self.load_seats()  # Refresh to show seats as red now
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Booking failed: {e}")
        finally:
            cur.close()
            conn.close()