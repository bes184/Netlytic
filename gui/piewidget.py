import sys
import math

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

class PieWidget(QWidget):
    clicked = pyqtSignal()
    def __init__(self, start_angle=30, span_angle=120, outline=Qt.blue, color=Qt.blue, parent=None):
        super().__init__(parent)
        self.start_angle = start_angle  # Start angle in degrees
        self.span_angle = span_angle  # Span angle in degrees
        self.outline = outline
        self.color = color

        self.is_pressed = False
        self.pressed_outline = QColor(Qt.white)

        # self.click_pos = None

        self.setStyleSheet("background: transparent;")
        # self.setMask(self.create_mask())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Circle dimensions
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = min(center_x, center_y) * 0.8
        rect = QRectF(center_x - radius, center_y - radius, 2 * radius, 2 * radius)

        current_outline = self.pressed_outline if self.is_pressed else self.outline

        # Draw arc
        painter.setPen(QPen(current_outline, 2))
        painter.setBrush(Qt.NoBrush)  # No fill
        painter.drawArc(rect, self.start_angle * 16, self.span_angle * 16)  # Angles in 1/16 degree

        # Draw filled pie
        painter.setBrush(QBrush(self.color))
        painter.drawPie(rect, self.start_angle * 16, self.span_angle * 16)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_inside_slice(event.pos()):
            self.is_pressed = True  # Set pressed state
            self.update()  # Trigger repaint
            # self.click_pos = event.pos()
            self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_pressed = False  # Reset pressed state
            self.update()  # Trigger repaint

    def is_inside_slice(self, pos):
        """Check if the mouse position is inside the pie slice."""
        center_x = self.width() / 2
        center_y = self.height() / 2

        # Convert to relative coordinates
        dx = pos.x() - center_x
        dy = pos.y() - center_y
        distance = math.sqrt(dx**2 + dy**2)

        # Check if within radius
        radius = min(center_x, center_y) * 0.8
        if distance > radius:
            return False

        # Calculate angle in degrees (polar coordinates)
        angle = math.degrees(math.atan2(-dy, dx))  # atan2 returns radians; -dy flips Y-axis
        angle = angle % 360  # Ensure angle is between 0 and 360

        # Normalize start and end angles of the slice
        start = self.start_angle % 360
        end = (self.start_angle + self.span_angle) % 360

        # Handle angle wrapping (if the pie slice crosses 0 degrees)
        if start < end:
            return start <= angle <= end
        else:
            return angle >= start or angle <= end

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pie Slice Click Test")
        self.setGeometry(100, 100, 400, 400)

        # Create PieWidget instances for multiple slices
        self.pie1 = PieWidget(start_angle=0, span_angle=90, outline=Qt.black, color=Qt.red, parent=self)
        self.pie1.setGeometry(100, 100, 200, 200)
        self.pie1.clicked.connect(lambda: print("Pie Slice 1 clicked"))

        self.pie2 = PieWidget(start_angle=90, span_angle=90, outline=Qt.black, color=Qt.green, parent=self)
        self.pie2.setGeometry(100, 100, 200, 200)  # Overlays pie1
        self.pie2.clicked.connect(lambda: print("Pie Slice 2 clicked"))

        self.pie3 = PieWidget(start_angle=180, span_angle=90, outline=Qt.black, color=Qt.blue, parent=self)
        self.pie3.setGeometry(100, 100, 200, 200)  # Overlays pie1
        self.pie3.clicked.connect(lambda: print("Pie Slice 3 clicked"))

        self.pie4 = PieWidget(start_angle=270, span_angle=90, outline=Qt.black, color=Qt.yellow, parent=self)
        self.pie4.setGeometry(100, 100, 200, 200)  # Overlays pie1
        self.pie4.clicked.connect(lambda: print("Pie Slice 4 clicked"))

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())