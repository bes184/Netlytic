import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

class PieWidget(QWidget):
    def __init__(self, start_angle=30, span_angle=120, outline=Qt.blue, color=Qt.blue, parent=None):
        super().__init__(parent)
        self.start_angle = start_angle  # Start angle in degrees
        self.span_angle = span_angle  # Span angle in degrees
        self.outline = outline
        self.color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Circle dimensions
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = min(center_x, center_y) * 0.8
        rect = QRectF(center_x - radius, center_y - radius, 2 * radius, 2 * radius)

        # Draw arc
        painter.setPen(QPen(self.outline, 2))
        painter.setBrush(Qt.NoBrush)  # No fill
        painter.drawArc(rect, self.start_angle * 16, self.span_angle * 16)  # Angles in 1/16 degree

        # Draw filled pie
        painter.setBrush(QBrush(self.color))
        painter.drawPie(rect, self.start_angle * 16, self.span_angle * 16)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PieWidget()
    widget.show()
    sys.exit(app.exec_())
