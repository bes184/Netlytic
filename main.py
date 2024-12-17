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

import sys
from PyQt5.QtWidgets import QApplication
from gui import screen

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create an instance of MainWindow
    window = screen.MainWindow()

    # Start the event loop
    sys.exit(app.exec_())