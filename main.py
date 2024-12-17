from network_functions import find_devices
from network_functions import get_http_traffic
import os

# curr_ip = find_devices.get_current_ip()
# find_devices.scan_network(curr_ip)
# input("enter")
# # curr_hostname = find_devices.get_hostname(curr_ip)
# ip_list = []
# sni_list = []
# # print(f"IP: {curr_ip}, Hostname: {curr_hostname}")
# http_ips = get_http_traffic.start_sniff(curr_ip)
# print(http_ips)
# input("enter")

from gui import splashscreen
from gui import screen

import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
import os

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