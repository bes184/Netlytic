import math
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

class CirclePolygonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.num_sides = 30  # Number of sides for the polygon

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Smooth the polygon

        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = min(center_x, center_y) * 0.8

        points = QPolygonF()
        for i in range(self.num_sides):
            angle = 2 * math.pi * i / self.num_sides
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append(QPointF(x, y))

        # Draw the polygon
        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(QBrush(Qt.blue))
        painter.drawPolygon(points)

class FractionCircleWidget(QWidget):
    def __init__(self, start_angle=30, span_angle=120, outline=Qt.blue, color=Qt.blue):
        super().__init__()
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

class PolygonWidget(QWidget):
    def __init__(self,parent=None, points=[], outline=Qt.blue, color=Qt.blue):
        super().__init__(parent)
        self.points = points
        self.outline = outline
        self.color = color
        self.clicked = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(self.outline, 2, Qt.SolidLine))
        painter.setBrush(QBrush(self.color))

        # Define the triangle's points
        points = QPolygonF()
        for point in self.points:
            (x, y) = point
            points.append(QPointF(x, y))

        # Draw the triangle
        painter.drawPolygon(points)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(f"Polygon clicked at position: {event.pos()}")
            self.clicked = not self.clicked  # Example toggle state
            temp_color = self.color
            self.color = self.outline
            self.outline = temp_color
            self.update()  # Trigger a repaint if necessary

def hex_to_qcolor(hex_string):
        # Remove the '#' if it exists
        hex_string = hex_string.lstrip('#')

        # Convert the hex string to an integer
        rgb = int(hex_string, 16)

        # Extract the RGB values
        r = (rgb >> 16) & 0xFF
        g = (rgb >> 8) & 0xFF
        b = rgb & 0xFF
        return QColor(r, g, b)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.width, self.height = screen_geometry.width(), screen_geometry.height()
        self.width = int(self.width*0.6)
        self.height = int(self.height*0.6)
        self.setFixedSize(self.width, self.height)

        # setting title
        self.setWindowTitle("test")

        self.homepage_container = QWidget(self)
        self.homepage_container.setGeometry(0, 0,
                                        self.width,
                                        self.height)
        
        self.homepage_layout = QHBoxLayout(self.homepage_container)

        self.piechart_container = QWidget(self.homepage_container)
        self.piechart_container.setStyleSheet("background: red")
        self.homepage_layout.addWidget(self.piechart_container)
        self.piechart_layout = QVBoxLayout(self.piechart_container)

        self.deviceinfo_container = QWidget(self.homepage_container)
        self.deviceinfo_container.setStyleSheet("background: black")
        self.homepage_layout.addWidget(self.deviceinfo_container)
        self.deviceinfo_layout = QVBoxLayout(self.deviceinfo_container)

        self.show()
    #     # Set the background color to grey
    #     self.setStyleSheet("background-color: black;") 


    #     self.menu_widgets = []  # Store your widgets

    #     self.aLabel = QLabel("A label", self)
    #     self.aLabel.setStyleSheet("color:white")
    #     self.aLabel.move(int(self.width/2), 0)

    #      # Create a layout for the main window (if it doesn't already have one)

    #     # Create a sample PolygonWidget
    #     points = [
    #         (150, 50),
    #         (50, 50),
    #         (150, 150)
    #     ]
    #     self.upperTriangle = PolygonWidget(points=points, outline=Qt.red, color=Qt.green, parent=self)
        
    #     self.upperTriangle.setGeometry(50, 50, 200, 200)
        
    #     self.upperTriangle2 = PolygonWidget(points=points, outline=Qt.red, color=Qt.red, parent=self)
    #     self.upperTriangle2.setGeometry(150, 150, 200, 200)

       
    #     self.upperTriangle.show()
    #     self.upperTriangle2.show()

    #     self.aButton = QPushButton("push", self)
    #     self.aButton.setStyleSheet("background:white; color:black;border:1px solid red")

    #     # self.upperTriangle.move(0,0)
    #     # self.upperTriangle2.move(30,0)
    #     self.aButton.move(int(self.width/2), int(self.height/2))
    #     self.aButton.show()

    #     self.aButton.clicked.connect(lambda: self.showTriangle())
        
    #     self.show()

    #     self.someTriangle()

    # def someTriangle(self):
    #     points = [
    #     (50, 50),
    #     (150, 50),
    #     (150, 150)
    #     ]
    #     self.aTriangle = PolygonWidget(points=points, outline=Qt.red, color=Qt.red, parent=self)
    #     self.aTriangle.setGeometry(250, 250, 200, 200)
    #     self.aTriangle.hide()

    # def showTriangle(self):
    #     if self.upperTriangle2.isVisible():
    #         print("vis", self.upperTriangle.isVisible())
    #         # self.upperTriangle2.setVisible(False)
    #         # self.upperTriangle2.show()
    #         self.upperTriangle2.hide()
    #         self.aTriangle.show()
                
    #     else:
    #         print("invis", self.upperTriangle.isVisible())
    #         # self.upperTriangle2.setVisible(True) 
    #         self.upperTriangle2.show()
    #         self.aTriangle.hide()
            

if __name__ == '__main__':
    aQColor = hex_to_qcolor("#CC7722")
    app = QApplication(sys.argv)
    # widget = FractionCircleWidget(start_angle=0, span_angle=360, outline=Qt.white, color=aQColor)
    # widget = PolygonWidget()
    window = MainWindow()
    # app.exec_()
    sys.exit(app.exec_())
