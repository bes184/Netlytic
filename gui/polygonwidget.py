import sys

# import custom_gui_functions as cgf

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

class PolygonWidget(QWidget):
    def __init__(self, parent=None, points=[], outline=Qt.blue, color=Qt.blue):
        super().__init__(parent)
        self.points = points
        self.outline = outline
        self.color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(self.outline, 2, Qt.SolidLine))
        painter.setBrush(QBrush(self.color))

        points = QPolygonF()
        for point in self.points:
            (x, y) = point
            points.append(QPointF(x, y))

        painter.drawPolygon(points)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    points = [(103, 160),
                (257, 160),
                (103, 111)]
    widget = PolygonWidget(points=points)
    widget.show()
    widget2 = PolygonWidget(points=points)
    # cgf.place_down(widget2, widget)
    widget2.show()
    sys.exit(app.exec_())