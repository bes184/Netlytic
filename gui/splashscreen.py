from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.width, self.height = screen_geometry.width(), screen_geometry.height()
        self.width = int(self.width*0.3)
        self.height = int(self.height*0.3)

        self.setPixmap(QPixmap('gui/images/splash.png').scaled(self.width, self.height, Qt.AspectRatioMode.KeepAspectRatio))
        self.show()

