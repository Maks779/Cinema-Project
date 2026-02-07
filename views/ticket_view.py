import os
import qrcode
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QGraphicsDropShadowEffect,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor, QImage, QPageSize
from PySide6.QtCore import Qt, QRectF
from PySide6.QtPrintSupport import QPrinter


class TicketView(QWidget):
    def __init__(self, user_id, username, role, booking_details):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.role = role
        self.details = booking_details

        self.setWindowTitle("Your Ticket")
        icon_path = "assets/cinema_logo.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setup_background()

        self.showMaximized()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 50)
        self.main_layout.setSpacing(20)

        top_bar = QHBoxLayout()

        self.btn_back = QPushButton("← Back")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setFixedSize(120, 45)
        self.apply_glass_style(self.btn_back)
        self.btn_back.clicked.connect(self.go_to_menu)

        top_bar.addWidget(self.btn_back)
        top_bar.addStretch()
        self.main_layout.addLayout(top_bar)

        self.main_layout.addStretch()

        center_row = QHBoxLayout()
        center_row.addStretch()

        self.ticket_card = QFrame()
        self.ticket_card.setFixedWidth(400)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(80)
        shadow.setXOffset(0)
        shadow.setYOffset(20)
        shadow.setColor(QColor(0, 0, 0, 200))
        self.ticket_card.setGraphicsEffect(shadow)

        self.ticket_card.setStyleSheet(
            """
            QFrame {
                background-color: #ffffff;
                border-radius: 24px;
            }
        """
        )

        card_layout = QVBoxLayout(self.ticket_card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(130)
        header.setStyleSheet(
            """
            QFrame {
                background-color: #ffb400;
                border-top-left-radius: 24px;
                border-top-right-radius: 24px;
            }
        """
        )
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(8)

        if os.path.exists(icon_path):
            logo_lbl = QLabel()
            pix = QPixmap(icon_path)
            logo_lbl.setPixmap(
                pix.scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            logo_lbl.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(logo_lbl)

        lbl_confirmed = QLabel("BOOKING CONFIRMED")
        lbl_confirmed.setStyleSheet(
            "color: #000; font-size: 13px; font-weight: 800; letter-spacing: 2px;"
        )
        header_layout.addWidget(lbl_confirmed)
        card_layout.addWidget(header)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(30, 25, 30, 15)
        body_layout.setSpacing(15)

        lbl_movie = QLabel(self.details.get("movie", "Movie").upper())
        lbl_movie.setWordWrap(True)
        lbl_movie.setAlignment(Qt.AlignCenter)
        lbl_movie.setStyleSheet(
            "color: #111; font-size: 20px; font-weight: 900; font-family: 'Arial Black'; border: none;"
        )
        body_layout.addWidget(lbl_movie)

        info_grid = QVBoxLayout()
        info_grid.setSpacing(12)

        self.add_detail_row(info_grid, "DATE", self.details.get("date", "-"))
        self.add_detail_row(info_grid, "TIME", self.details.get("time", "-"))

        seats_list = self.details.get("seats", [])
        seats_str = ", ".join(seats_list) if seats_list else "-"
        self.add_detail_row(info_grid, "SEATS", seats_str, highlight=True)

        body_layout.addLayout(info_grid)
        card_layout.addWidget(body)

        qr_box = QWidget()
        qr_box.setStyleSheet(
            "background: white; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px;"
        )
        qr_lay = QVBoxLayout(qr_box)
        qr_lay.setContentsMargins(0, 10, 0, 30)
        qr_lay.setAlignment(Qt.AlignCenter)

        qr_pix = self.generate_qr("https://google.com")
        qr_lbl = QLabel()
        qr_lbl.setPixmap(qr_pix)
        qr_lbl.setStyleSheet("border: none;")
        qr_lay.addWidget(qr_lbl)

        hint = QLabel("Scan at entrance")
        hint.setStyleSheet(
            "color: #999; font-size: 11px; margin-top: 5px; border: none;"
        )
        hint.setAlignment(Qt.AlignCenter)
        qr_lay.addWidget(hint)
        card_layout.addWidget(qr_box)

        center_row.addWidget(self.ticket_card)
        center_row.addStretch()

        self.main_layout.addLayout(center_row)
        self.main_layout.addStretch()

        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()

        self.btn_download = QPushButton("Download PDF Ticket")
        self.btn_download.setCursor(Qt.PointingHandCursor)
        self.btn_download.setFixedSize(240, 55)
        self.apply_glass_style(self.btn_download, primary=True)
        self.btn_download.clicked.connect(self.save_pdf)

        bottom_bar.addWidget(self.btn_download)
        bottom_bar.addStretch()

        self.main_layout.addLayout(bottom_bar)

    def setup_background(self):
        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)

        possible_paths = [
            "assets/bg_photo3.png",
            "assets/bg_photo2.png",
            "assets/bg_photo.png",
        ]

        pixmap = None
        for path in possible_paths:
            if os.path.exists(path):
                pixmap = QPixmap(path)
                break

        if pixmap and not pixmap.isNull():
            self.bg_label.setPixmap(pixmap)
        else:
            self.bg_label.setStyleSheet(
                "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #111, stop:1 #222);"
            )

        self.bg_label.lower()

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")
        self.overlay.lower()

    def resizeEvent(self, event):
        if hasattr(self, "bg_label"):
            self.bg_label.resize(self.size())
        if hasattr(self, "overlay"):
            self.overlay.resize(self.size())
        super().resizeEvent(event)

    def apply_glass_style(self, button, primary=False):
        if primary:
            bg_color = "rgba(255, 180, 0, 0.2)"
            border_color = "rgba(255, 180, 0, 0.6)"
            hover_bg = "rgba(255, 180, 0, 0.4)"
            text_color = "#ffb400"
            radius = "27px"
        else:
            bg_color = "rgba(255, 255, 255, 0.1)"
            border_color = "rgba(255, 255, 255, 0.3)"
            hover_bg = "rgba(255, 255, 255, 0.25)"
            text_color = "#ffffff"
            radius = "15px"

        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: {radius}; /* Повністю круглі боки */
                font-size: 15px;
                font-weight: bold;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                border: 1px solid {text_color};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: {border_color};
            }}
        """
        )

    def add_detail_row(self, layout, label_text, value_text, highlight=False):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setStyleSheet(
            "color: #888; font-size: 13px; font-weight: bold; border: none;"
        )

        val = QLabel(value_text)
        if highlight:
            val.setStyleSheet(
                "color: #ffb400; font-size: 18px; font-weight: bold; background-color: #222; border-radius: 6px; padding: 4px 8px;"
            )
        else:
            val.setStyleSheet(
                "color: #000; font-size: 16px; font-weight: bold; border: none;"
            )

        val.setAlignment(Qt.AlignRight)
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(val)
        layout.addLayout(row)

        if not highlight:
            line = QFrame()
            line.setFixedHeight(1)
            line.setStyleSheet("background-color: #f0f0f0; border: none;")
            layout.addWidget(line)

    def generate_qr(self, data):
        try:
            qr = qrcode.QRCode(version=1, box_size=6, border=1)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            im_data = img.convert("RGBA").tobytes("raw", "RGBA")
            qim = QImage(im_data, img.size[0], img.size[1], QImage.Format_RGBA8888)
            return QPixmap.fromImage(qim)

        except Exception as e:
            print(f"QR Error: {e}")
            pix = QPixmap(140, 140)
            pix.fill(Qt.white)
            painter = QPainter(pix)
            painter.setPen(Qt.black)
            painter.drawRect(5, 5, 130, 130)
            painter.drawText(pix.rect(), Qt.AlignCenter, "QR CODE")
            painter.end()
            return pix

    def save_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Ticket",
            f"Ticket_{self.details.get('movie', 'Cinema')}.pdf",
            "PDF Files (*.pdf)",
        )
        if filename:
            try:
                self.ticket_card.setGraphicsEffect(None)

                pixmap = self.ticket_card.grab()

                shadow = QGraphicsDropShadowEffect(self)
                shadow.setBlurRadius(80)
                shadow.setXOffset(0)
                shadow.setYOffset(20)
                shadow.setColor(QColor(0, 0, 0, 200))
                self.ticket_card.setGraphicsEffect(shadow)

                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(filename)
                printer.setPageSize(QPageSize(QPageSize.A4))

                painter = QPainter(printer)
                page_rect = printer.pageRect(QPrinter.DevicePixel)

                target_width = page_rect.width() * 0.55
                scale = target_width / pixmap.width()
                target_height = pixmap.height() * scale

                x = (page_rect.width() - target_width) / 2
                y = (page_rect.height() - target_height) / 3

                painter.drawPixmap(
                    QRectF(x, y, target_width, target_height),
                    pixmap,
                    QRectF(pixmap.rect()),
                )
                painter.end()

                QMessageBox.information(self, "Success", f"Ticket saved successfully!")

            except Exception as e:
                shadow = QGraphicsDropShadowEffect(self)
                shadow.setBlurRadius(80)
                shadow.setColor(QColor(0, 0, 0, 200))
                self.ticket_card.setGraphicsEffect(shadow)

                QMessageBox.critical(self, "Error", f"Failed to save PDF: {e}")

    def go_to_menu(self):
        from views.main_view import MainView

        self.mw = MainView(self.user_id, self.username, self.role)
        self.mw.showMaximized()
        self.close()
