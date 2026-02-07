import os
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QComboBox,
    QMessageBox,
    QFrame,
    QSizePolicy,
    QScrollArea,
)
from PySide6.QtGui import QPixmap, QCursor, QIcon, QPainter, QPainterPath
from PySide6.QtCore import Qt, QRectF
from db.connection import get_db_connection


class ShowtimeView(QWidget):
    def __init__(
        self,
        movie_id,
        movie_title,
        user_id=None,
        username="Guest",
        role="guest",
        description=None,
    ):
        super().__init__()
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.user_id = user_id
        self.username = username
        self.role = role
        self.description = description

        self.movie_genre = "Action / Sci-Fi"
        self.movie_duration = "2h 15m"

        self.selected_seats = []
        self.showtimes_data = []

        self.premium_surcharge = 5.0
        self.premium_rows_start_index = 6

        self.setWindowTitle(f"Booking: {movie_title}")
        icon_path = "assets/cinema_logo.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_background()

        left_scroll_area = QScrollArea()
        left_scroll_area.setFixedWidth(400)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setFrameShape(QFrame.NoFrame)
        left_scroll_area.setStyleSheet(
            """
            QScrollArea {
                background-color: rgba(0, 0, 0, 0.6);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0,0,0,0.3);
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.2);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
        )

        left_content_widget = QWidget()
        left_content_widget.setStyleSheet("background: transparent;")

        left_layout = QVBoxLayout(left_content_widget)
        left_layout.setContentsMargins(30, 40, 30, 40)
        left_layout.setSpacing(20)

        btn_back = QPushButton("← Back to Movies")
        btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        btn_back.setStyleSheet(
            """
            QPushButton {
                color: #aaa;
                background: transparent;
                border: 1px solid #555;
                border-radius: 15px;
                padding: 8px 15px;
                font-size: 13px;
                text-align: left;
            }
            QPushButton:hover {
                color: white;
                border-color: white;
                background: rgba(255, 255, 255, 0.1);
            }
        """
        )
        btn_back.clicked.connect(self.go_back_to_movies)
        left_layout.addWidget(btn_back)

        poster_pix = self.load_local_poster()
        poster_lbl = QLabel()
        poster_lbl.setFixedSize(320, 460)
        poster_lbl.setAlignment(Qt.AlignCenter)
        poster_lbl.setStyleSheet("background: transparent; border: none;")

        if poster_pix:
            scaled = poster_pix.scaled(
                poster_lbl.width(),
                poster_lbl.height(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation,
            )
            poster_lbl.setPixmap(self.make_rounded_pixmap(scaled, radius=18))
        else:
            poster_lbl.setText("No poster")
            poster_lbl.setStyleSheet(
                "color: rgba(255,255,255,0.35); background: transparent; border: none;"
            )
        left_layout.addWidget(poster_lbl)

        lbl_title = QLabel(self.movie_title)
        lbl_title.setStyleSheet(
            "color: #ffb400; font-size: 32px; font-weight: bold; "
            "font-family: 'Segoe UI'; background: transparent; border: none;"
        )
        lbl_title.setWordWrap(True)
        left_layout.addWidget(lbl_title)

        lbl_meta = QLabel(f"{self.movie_genre} • {self.movie_duration}")
        lbl_meta.setStyleSheet(
            "color: #ddd; font-size: 14px; background: transparent; border: none;"
        )
        left_layout.addWidget(lbl_meta)

        desc_scroll = QLabel(
            self.description if self.description else "No description available."
        )
        desc_scroll.setStyleSheet(
            "color: #ccc; font-size: 14px; line-height: 1.4; background: transparent; border: none;"
        )
        desc_scroll.setWordWrap(True)
        desc_scroll.setAlignment(Qt.AlignTop)
        left_layout.addWidget(desc_scroll)

        left_layout.addStretch()
        left_scroll_area.setWidget(left_content_widget)
        self.main_layout.addWidget(left_scroll_area)

        right_container = QWidget()
        right_container.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(50, 40, 50, 40)
        right_layout.setSpacing(25)

        selectors_layout = QHBoxLayout()
        selectors_layout.setSpacing(20)

        self.date_combo = QComboBox()
        self.date_combo.setPlaceholderText("Select Date")
        self.date_combo.setFixedWidth(200)
        self.date_combo.setStyleSheet(
            """
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QComboBox:hover { border-color: #ffb400; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #222;
                color: white;
                selection-background-color: #ffb400;
                selection-color: black;
            }
        """
        )
        self.date_combo.currentIndexChanged.connect(self.on_date_changed)
        selectors_layout.addWidget(self.date_combo)

        self.time_combo = QComboBox()
        self.time_combo.setPlaceholderText("Select Time")
        self.time_combo.setFixedWidth(200)
        self.time_combo.setStyleSheet(self.date_combo.styleSheet())
        self.time_combo.currentIndexChanged.connect(self.load_seats)
        selectors_layout.addWidget(self.time_combo)

        selectors_layout.addStretch()

        user_lbl = QLabel(f"👤 {self.username}")
        user_lbl.setStyleSheet(
            "color: #ffb400; font-size: 14px; font-weight: bold; background: transparent; border: none;"
        )
        selectors_layout.addWidget(user_lbl)

        right_layout.addLayout(selectors_layout)

        self.placeholder_lbl = QLabel("Select Date & Time\nto view available seats")
        self.placeholder_lbl.setAlignment(Qt.AlignCenter)
        self.placeholder_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.placeholder_lbl.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.2);
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """
        )
        right_layout.addWidget(self.placeholder_lbl)

        self.booking_widgets = []

        self.screen_widget = QLabel("S  C  R  E  E  N")
        self.screen_widget.setAlignment(Qt.AlignCenter)
        self.screen_widget.setFixedHeight(40)
        self.screen_widget.setStyleSheet(
            """
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 rgba(255, 215, 120, 0.8),
                                       stop:0.4 rgba(255, 180, 60, 0.4),
                                       stop:1 rgba(255, 140, 0, 0));
            color: rgba(255, 220, 120, 0.95);
            font-weight: bold;
            font-size: 13px;
            border-top: 3px solid rgba(255, 190, 60, 0.9);
            border-radius: 6px;
        """
        )
        right_layout.addWidget(self.screen_widget)
        self.booking_widgets.append(self.screen_widget)

        self.seat_wrapper = QWidget()
        seat_wrapper_layout = QHBoxLayout(self.seat_wrapper)
        seat_wrapper_layout.addStretch()

        self.seat_container = QWidget()
        self.seat_container.setStyleSheet(
            """
            QWidget {
                background-color: rgba(10, 10, 10, 0.75); 
                border: 1px solid rgba(255, 255, 255, 0.08); 
                border-radius: 30px; 
            }
        """
        )

        self.grid = QGridLayout(self.seat_container)
        self.grid.setSpacing(12)
        self.grid.setContentsMargins(40, 30, 40, 30)

        seat_wrapper_layout.addWidget(self.seat_container)
        seat_wrapper_layout.addStretch()
        right_layout.addWidget(self.seat_wrapper)
        self.booking_widgets.append(self.seat_wrapper)

        self.legend_widget = QWidget()
        self.legend_layout = QHBoxLayout(self.legend_widget)
        self.legend_layout.setContentsMargins(0, 0, 0, 0)
        self.legend_layout.addStretch()

        self.add_legend_item(
            self.legend_layout,
            "rgba(255, 140, 0, 0.25)",
            "Standard",
            border_color="rgba(255, 180, 60, 0.6)",
        )
        self.add_legend_item(
            self.legend_layout,
            "rgba(138, 43, 226, 0.25)",
            "Premium",
            border_color="rgba(147, 112, 219, 0.6)",
        )
        self.add_legend_item(self.legend_layout, "#ffb400", "Selected")
        self.add_legend_item(self.legend_layout, "rgba(0, 0, 0, 0.5)", "Taken")

        self.legend_layout.addStretch()
        right_layout.addWidget(self.legend_widget)
        self.booking_widgets.append(self.legend_widget)

        right_layout.addStretch()

        self.footer_widget = QWidget()
        self.footer_layout = QHBoxLayout(self.footer_widget)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)

        self.price_lbl = QLabel("Total: $0.00")
        self.price_lbl.setStyleSheet(
            "color: white; font-size: 24px; font-weight: bold; background: transparent; border: none;"
        )
        self.footer_layout.addWidget(self.price_lbl)

        self.footer_layout.addStretch()

        self.confirm_btn = QPushButton("Select Seats")
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.setFixedSize(220, 50)
        self.confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.confirm_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #ffb400;
                color: #000;
                font-weight: bold;
                font-size: 16px;
                border-radius: 25px;
            }
            QPushButton:hover { background-color: #ffc947; }
            QPushButton:disabled { background-color: #444; color: #777; }
        """
        )
        self.confirm_btn.clicked.connect(self.process_booking)
        self.footer_layout.addWidget(self.confirm_btn)

        right_layout.addWidget(self.footer_widget)
        self.booking_widgets.append(self.footer_widget)

        self.main_layout.addWidget(right_container)

        self.hide_booking_interface()

        self.load_dates()

    def hide_booking_interface(self):
        for w in self.booking_widgets:
            w.setVisible(False)
        self.placeholder_lbl.setVisible(True)

    def show_booking_interface(self):
        self.placeholder_lbl.setVisible(False)
        for w in self.booking_widgets:
            w.setVisible(True)

    def setup_background(self):
        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)
        bg_path = "assets/bg_photo3.png"
        if not os.path.exists(bg_path):
            bg_path = "assets/bg_photo2.png"
        if not os.path.exists(bg_path):
            bg_path = "assets/bg_photo.png"

        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path))
        else:
            self.bg_label.setStyleSheet("background-color: #111;")
        self.bg_label.lower()

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.85);")
        self.overlay.lower()

    def resizeEvent(self, event):
        if hasattr(self, "bg_label") and self.bg_label:
            self.bg_label.resize(self.size())
        if hasattr(self, "overlay") and self.overlay:
            self.overlay.resize(self.size())
        super().resizeEvent(event)

    def add_legend_item(
        self, layout, color, text, border_color="rgba(255,255,255,0.1)"
    ):
        container = QHBoxLayout()
        box = QLabel()
        box.setFixedSize(16, 16)
        box.setStyleSheet(
            f"background-color: {color}; border-radius: 4px; border: 1px solid {border_color};"
        )
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color: #ccc; font-size: 13px; background: transparent; border: none;"
        )
        container.addWidget(box)
        container.addWidget(lbl)
        container.addSpacing(15)
        layout.addLayout(container)

    def load_dates(self):
        self.date_combo.clear()
        conn = get_db_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT start_time::date FROM showtimes 
            WHERE movie_id = %s ORDER BY start_time::date
        """,
            (self.movie_id,),
        )
        dates = cur.fetchall()

        if not dates:
            self.date_combo.addItem("No dates available")
            self.date_combo.setEnabled(False)
        else:
            self.date_combo.setEnabled(True)
            for d in dates:
                date_str = d[0].strftime("%Y-%m-%d")
                display_str = d[0].strftime("%d %b %Y")
                self.date_combo.addItem(display_str, date_str)
        cur.close()
        conn.close()
        self.on_date_changed()

    def on_date_changed(self):
        self.time_combo.clear()
        self.hide_booking_interface()

        idx = self.date_combo.currentIndex()
        if idx < 0:
            return

        selected_date_str = self.date_combo.currentData()
        conn = get_db_connection()
        if not conn:
            return
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, hall_id, start_time, price 
            FROM showtimes 
            WHERE movie_id = %s AND start_time::date = %s
            ORDER BY start_time
        """,
            (self.movie_id, selected_date_str),
        )

        self.showtimes_data = cur.fetchall()

        if not self.showtimes_data:
            self.time_combo.addItem("No showtimes")
            self.time_combo.setEnabled(False)
        else:
            self.time_combo.setEnabled(True)
            for row in self.showtimes_data:
                time_obj = row[2]
                time_display = time_obj.strftime("%H:%M")
                self.time_combo.addItem(time_display)

            self.time_combo.setCurrentIndex(0)
            self.load_seats()

        cur.close()
        conn.close()

    def load_seats(self):
        if self.time_combo.currentIndex() < 0 or not self.showtimes_data:
            self.hide_booking_interface()
            return

        self.show_booking_interface()

        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.selected_seats = []
        self.update_price()

        showtime_idx = self.time_combo.currentIndex()
        if showtime_idx >= len(self.showtimes_data):
            return

        showtime_id = self.showtimes_data[showtime_idx][0]

        conn = get_db_connection()
        taken_seats = []
        if conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT bs.seat_number 
                FROM booked_seats bs
                JOIN bookings b ON bs.booking_id = b.id
                WHERE b.showtime_id = %s
            """,
                (showtime_id,),
            )
            taken_seats = [r[0] for r in cur.fetchall()]
            cur.close()
            conn.close()

        rows = 8
        cols = 10

        for r in range(rows):
            is_premium = r >= self.premium_rows_start_index
            row_char = chr(65 + r)
            lbl = QLabel(row_char)
            color = "#bd93f9" if is_premium else "rgba(255,255,255,0.3)"
            lbl.setStyleSheet(
                f"color: {color}; font-weight: bold; background: transparent; border: none;"
            )
            lbl.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(lbl, r, 0)

            for c in range(cols):
                seat_num = f"{row_char}{c+1}"
                btn = QPushButton()
                btn.setFixedSize(36, 36)
                btn.setCursor(QCursor(Qt.PointingHandCursor))

                style_taken = """
                    background-color: rgba(0, 0, 0, 0.5);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                """
                style_standard = """
                    QPushButton {
                        background-color: rgba(255, 140, 0, 0.25);
                        border: 1px solid rgba(255, 180, 60, 0.6);
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 160, 40, 0.45);
                        border-color: rgba(255, 200, 100, 0.9);
                    }
                    QPushButton:checked {
                        background-color: #ffb400;
                        border: none;
                    }
                """
                style_premium = """
                    QPushButton {
                        background-color: rgba(138, 43, 226, 0.25);
                        border: 1px solid rgba(147, 112, 219, 0.6);
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: rgba(148, 53, 236, 0.45);
                        border-color: rgba(180, 150, 250, 0.9);
                    }
                    QPushButton:checked {
                        background-color: #ffb400; 
                        border: none;
                    }
                """

                if seat_num in taken_seats:
                    btn.setEnabled(False)
                    btn.setStyleSheet(style_taken)
                else:
                    btn.setCheckable(True)
                    btn.setStyleSheet(style_premium if is_premium else style_standard)
                    btn.clicked.connect(
                        lambda ch, s=seat_num, p=is_premium: self.toggle_seat(s, p)
                    )

                self.grid.addWidget(btn, r, c + 1)

    def toggle_seat(self, seat_num, is_premium):
        if seat_num in self.selected_seats:
            self.selected_seats.remove(seat_num)
        else:
            self.selected_seats.append(seat_num)
        self.update_price()

    def update_price(self):
        total = 0.0
        if self.time_combo.currentIndex() >= 0 and self.showtimes_data:
            base_price = float(self.showtimes_data[self.time_combo.currentIndex()][3])
            for seat in self.selected_seats:
                row_char = seat[0]
                row_idx = ord(row_char) - 65
                if row_idx >= self.premium_rows_start_index:
                    total += base_price + self.premium_surcharge
                else:
                    total += base_price

        self.price_lbl.setText(f"Total: ${total:.2f}")

        count = len(self.selected_seats)
        if count > 0:
            self.confirm_btn.setText(f"Book {count} Ticket{'s' if count > 1 else ''}")
            self.confirm_btn.setEnabled(True)
            self.confirm_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #ffb400;
                    color: #000;
                    font-weight: bold;
                    font-size: 16px;
                    border-radius: 25px;
                }
                QPushButton:hover { background-color: #ffc947; }
            """
            )
        else:
            self.confirm_btn.setText("Select Seats")
            self.confirm_btn.setEnabled(False)
            self.confirm_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: #777;
                    font-weight: bold;
                    font-size: 16px;
                    border-radius: 25px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
            """
            )

    def process_booking(self):
        if self.role == "guest":
            QMessageBox.information(
                self, "Login Required", "Please log in to book tickets."
            )
            from views.login_window import LoginWindow

            self.lw = LoginWindow()
            self.lw.show()
            self.close()
            return

        if not self.selected_seats:
            return

        conn = get_db_connection()
        if not conn:
            return
        cur = conn.cursor()

        try:
            idx = self.time_combo.currentIndex()
            showtime_id = self.showtimes_data[idx][0]
            base_price = float(self.showtimes_data[idx][3])

            total_price = 0.0
            for seat in self.selected_seats:
                row_idx = ord(seat[0]) - 65
                if row_idx >= self.premium_rows_start_index:
                    total_price += base_price + self.premium_surcharge
                else:
                    total_price += base_price

            cur.execute(
                """
                INSERT INTO bookings (user_id, showtime_id, total_price)
                VALUES (%s, %s, %s) RETURNING id
            """,
                (self.user_id, showtime_id, total_price),
            )
            booking_id = cur.fetchone()[0]

            for seat in self.selected_seats:
                cur.execute(
                    """
                    INSERT INTO booked_seats (booking_id, seat_number)
                    VALUES (%s, %s)
                """,
                    (booking_id, seat),
                )

            conn.commit()

            booking_info = {
                "movie": self.movie_title,
                "date": self.date_combo.currentText(),
                "time": self.time_combo.currentText(),
                "seats": self.selected_seats,
                "total": total_price,
                "poster_id": self.movie_id,
            }

            from views.ticket_view import TicketView

            self.ticket_window = TicketView(
                self.user_id, self.username, self.role, booking_info
            )
            self.ticket_window.show()
            self.close()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Booking failed: {e}")
        finally:
            cur.close()
            conn.close()

    def load_local_poster(self):
        poster_path = f"posters_cache/movie_{self.movie_id}.jpg"
        if os.path.exists(poster_path):
            pix = QPixmap(poster_path)
            if not pix.isNull():
                return pix
        return None

    def make_rounded_pixmap(self, pixmap, radius=18):
        if pixmap is None or pixmap.isNull():
            return pixmap
        target = QPixmap(pixmap.size())
        target.fill(Qt.transparent)
        painter = QPainter(target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        path = QPainterPath()
        path.addRoundedRect(
            QRectF(0, 0, pixmap.width(), pixmap.height()), radius, radius
        )
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return target

    def go_back_to_movies(self):
        from views.main_view import MainView

        self.mw = MainView(self.user_id, self.username, self.role)
        self.mw.showMaximized()
        self.close()
