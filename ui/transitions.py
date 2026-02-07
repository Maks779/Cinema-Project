from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget


def fade_to_window(current: QWidget, next_cls, *args, **kwargs):
    next_win = next_cls(*args, **kwargs)
    next_win.setWindowOpacity(0.0)
    next_win.setGeometry(current.geometry())
    next_win.show()

    anim_out = QPropertyAnimation(current, b"windowOpacity")
    anim_out.setDuration(300)
    anim_out.setStartValue(1.0)
    anim_out.setEndValue(0.0)
    anim_out.setEasingCurve(QEasingCurve.InOutQuad)

    anim_in = QPropertyAnimation(next_win, b"windowOpacity")
    anim_in.setDuration(300)
    anim_in.setStartValue(0.0)
    anim_in.setEndValue(1.0)
    anim_in.setEasingCurve(QEasingCurve.InOutQuad)

    def close_current():
        current.close()

    anim_out.finished.connect(close_current)

    anim_out.start()
    anim_in.start()

    return next_win
