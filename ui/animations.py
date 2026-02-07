from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtWidgets import QGraphicsOpacityEffect


def fade_in(widget, duration=400):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity")
    animation.setDuration(duration)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    animation.start()

    widget._fade_animation = animation
    return animation


def slide_in_from_bottom(widget, duration=500):
    parent_height = widget.parent().height() if widget.parent() else 800
    start_pos = QPoint(widget.x(), parent_height)
    end_pos = widget.pos()

    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    animation.start()

    widget._slide_animation = animation
    return animation


def scale_up(widget, duration=400):
    animation = QPropertyAnimation(widget, b"geometry")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutCubic)

    start_geo = widget.geometry()
    end_geo = widget.geometry()

    start_geo.setWidth(int(end_geo.width() * 0.85))
    start_geo.setHeight(int(end_geo.height() * 0.85))

    animation.setStartValue(start_geo)
    animation.setEndValue(end_geo)
    animation.start()

    widget._scale_animation = animation
    return animation
