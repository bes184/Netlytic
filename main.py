import sys
import time
import os

from gui import splashscreen
from gui import screen

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = splashscreen.SplashScreen()
    
    for i in range(1, 101):
        time.sleep(0.02)  
        splash.showMessage(f"Loading... {i}%", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
        QApplication.processEvents()

    window = screen.MainWindow()
    window.show()
    splash.finish(window)

    sys.exit(app.exec())