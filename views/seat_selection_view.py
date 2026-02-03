from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt


class SeatSelectionView(QMainWindow):
    def __init__(self, showtime_id):
        super().__init__()
        self.setWindowTitle("Select Your Seats")
        self.setFixedSize(500, 650)  # Increased height slightly for the price label
        self.showtime_id = showtime_id
        self.selected_seats = []
        self.ticket_price = 25  # Price per seat in PLN

        layout = QVBoxLayout()

        # Screen Label
        label = QLabel("SCREEN")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-weight: bold; background-color: #34495e; color: white; padding: 5px;")
        layout.addWidget(label)

        # Seat Grid
        grid = QGridLayout()
        self.seat_buttons = {}

        for row in range(5):
            for col in range(8):
                seat_name = f"{chr(65 + row)}{col + 1}"
                btn = QPushButton(seat_name)
                btn.setCheckable(True)
                btn.setFixedSize(50, 50)
                # Available seats color: Green
                btn.setStyleSheet("background-color: #2ecc71; color: white;")
                btn.clicked.connect(lambda checked, s=seat_name: self.toggle_seat(s))

                grid.addWidget(btn, row, col)
                self.seat_buttons[seat_name] = btn

        layout.addLayout(grid)

        # --- NEW: PRICE LABEL ---
        self.price_label = QLabel("Total Price: 0 PLN")
        self.price_label.setAlignment(Qt.AlignCenter)
        self.price_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2ecc71; margin: 10px;")
        layout.addWidget(self.price_label)
        # ------------------------

        self.btn_confirm = QPushButton("Confirm Booking")
        self.btn_confirm.setFixedHeight(50)
        self.btn_confirm.setStyleSheet("background-color: #e67e22; color: white; font-weight: bold;")
        self.btn_confirm.clicked.connect(self.confirm_booking)
        layout.addWidget(self.btn_confirm)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_seat(self, seat_name):
        if seat_name in self.selected_seats:
            self.selected_seats.remove(seat_name)
            # Back to Green (Available)
            self.seat_buttons[seat_name].setStyleSheet("background-color: #2ecc71; color: white;")
        else:
            self.selected_seats.append(seat_name)
            # Yellow/Gold for Selected
            self.seat_buttons[seat_name].setStyleSheet("background-color: #f1c40f; color: black;")

        # UPDATE PRICE DYNAMICALLY
        total = len(self.selected_seats) * self.ticket_price
        self.price_label.setText(f"Total Price: {total} PLN")

    def confirm_booking(self):
        if not self.selected_seats:
            QMessageBox.warning(self, "Warning", "Please select at least one seat!")
            return

        total_price = len(self.selected_seats) * self.ticket_price
        seats_str = ", ".join(self.selected_seats)

        QMessageBox.information(
            self,
            "Success",
            f"Booking Confirmed!\nSeats: {seats_str}\nTotal: {total_price} PLN\nEnjoy your movie!"
        )
        self.close()