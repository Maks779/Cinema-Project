from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt


class SeatSelectionView(QMainWindow):
    def __init__(self, showtime_id):
        super().__init__()
        self.setWindowTitle("Select Your Seats")
        self.setFixedSize(500, 600)
        self.showtime_id = showtime_id
        self.selected_seats = []

        layout = QVBoxLayout()
        label = QLabel("SCREEN")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-weight: bold; background-color: #34495e; color: white; padding: 5px;")
        layout.addWidget(label)

        grid = QGridLayout()
        self.seat_buttons = {}

        for row in range(5):
            for col in range(8):
                seat_name = f"{chr(65 + row)}{col + 1}"
                btn = QPushButton(seat_name)
                btn.setCheckable(True)
                btn.setFixedSize(50, 50)
                btn.setStyleSheet("background-color: #2ecc71; color: white;")
                btn.clicked.connect(lambda checked, s=seat_name: self.toggle_seat(s))

                grid.addWidget(btn, row, col)
                self.seat_buttons[seat_name] = btn

        layout.addLayout(grid)

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
            self.seat_buttons[seat_name].setStyleSheet("background-color: #2ecc71; color: white;")
        else:
            self.selected_seats.append(seat_name)
            self.seat_buttons[seat_name].setStyleSheet("background-color: #f1c40f; color: black;")

    def confirm_booking(self):
        if not self.selected_seats:
            QMessageBox.warning(self, "Warning", "Please select at least one seat!")
            return

        seats_str = ", ".join(self.selected_seats)
        QMessageBox.information(self, "Success", f"Booking Confirmed!\nSeats: {seats_str}\nEnjoy your movie!")
        self.close()