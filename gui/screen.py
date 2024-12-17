import sys
import threading
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

from gui import piewidget
from gui import custom_gui_functions as cgf
from network_functions import find_devices

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

class MainWindow(QMainWindow):
    
    # color variables
    colorDarkBlue = "#085394"
    colorDarkRed = "#CF2A27"
    colorDarkGreen = "#2E5339"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorWhite = "#FFFFFF"
    colorOrange = "#FFA500"
    colorDarkOrange = "#CC7722"
    colorBlack = "#000000"

    moduleName = "Netlytic"
    fontStyle = "Product Sans"
    theme1 = colorOrange
    theme2 = colorDarkOrange

    def __init__(self):
        super().__init__()

        # set screen size based on device screen size
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.width, self.height = screen_geometry.width(), screen_geometry.height()
        self.width = int(self.width*0.6)
        self.height = int(self.height*0.6)
        self.setFixedSize(self.width, self.height)

        # setting title
        self.setWindowTitle(self.moduleName)

        # Set the background color to grey
        self.setStyleSheet("background-color:"+self.colorMediumGrey+";") 

        self.header(self.theme1)
        self.side_bar(self.theme1)
        self.homepage()

        # Show the window
        self.show()

        self.menu(self.theme1)
        self.menu_styling(self.theme1)
    
    '''
    Header

    '''
    def header(self, bg):
        # Header block
        self.header_widgets = []

        self.header_block(bg)
        self.header_widgets.append(self.headerBlock)

        self.spacing = int(self.headerBlock.width()*0.005)
        self.iconSize = int(self.height*0.1*0.8)

        # AppName
        self.module_label(bg)
        self.header_widgets.append(self.moduleLabel)

        # Gear
        self.settings_label(bg)
        
        # signals
        self.settings.clicked.connect(lambda: self.gearClicked())

    def header_block(self, bg):
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(0, 0, self.width, int(self.height*0.1))
        self.headerBlock.setStyleSheet(
            "background-color:" + bg + ";"
        )
    
    def module_label(self, bg):
        self.moduleLabel = QLabel(self.moduleName, self)
        self.moduleLabel.setFont(QFont(self.fontStyle, int(self.headerBlock.height()*0.18)))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(
            int(self.spacing), 
            int(self.headerBlock.height()/2 - self.moduleLabel.height()))
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet(
            "background-color:" + bg + ";"
            "color:" + self.colorWhite
        )
    
    def settings_label(self, bg):
        self.settings = QPushButton(self)
        cgf.png_button(self.settings, "gear", self.iconSize)
        self.settings.move(
            int(self.headerBlock.width() - self.settings.width()), 
            int(self.headerBlock.height() / 2 - self.settings.height() / 2)
        )
        self.settings.setStyleSheet(
            "background-color:" + bg + ";"
            "border: 1px solid" + bg
        )
        self.settings_bg = bg

    '''
    Side Bar
    
    '''
    def side_bar(self, bg):
        # Side Bar block
        self.sidebar_widgets = []

        self.sidebar_block(bg)
        self.sidebar_widgets.append(self.sideBarBlock)

        # Hamburger
        self.hamburger_label(bg)
        self.sidebar_widgets.append(self.sideBar)

        # Home
        self.home_label(bg)
        self.sidebar_widgets.append(self.home)

        # Stats
        self.stats_label(bg)
        self.sidebar_widgets.append(self.stats)

        # signals 
        self.sideBar.clicked.connect(lambda: self.hamburgerClicked())
        self.home.clicked.connect(lambda: self.homeClicked())
        self.stats.clicked.connect(lambda: self.statsClicked())

        self.home.click()
    
    def sidebar_block(self, bg):
        self.sideBarBlock = QLabel(self)
        self.sideBarBlock.setGeometry(0, self.headerBlock.height(), 
                                 self.headerBlock.height(), int(self.height-self.headerBlock.height()))
        self.sideBarBlock.setStyleSheet(
            "background-color:" + bg + ";"
            "border: 1px solid" + bg
        )

    def hamburger_label(self, bg):
        self.sideBar = QPushButton(self)
        cgf.png_button(self.sideBar, "hamburger", self.iconSize)
        self.sideBar.move(
            int(self.spacing), 
            int(self.headerBlock.height() + self.spacing)
        )
        self.sideBar.setStyleSheet(
            "background-color:" + bg + ";"
            "border: 1px solid" + bg
        )
        self.sideBar_bg = bg

    def home_label(self, bg):
        self.home = QPushButton(self)
        cgf.png_button(self.home, "home", self.iconSize)
        self.home.move(
            int(self.spacing), 
            int(self.sideBar.y() + self.sideBar.height() + self.spacing)
        )
        self.home.setStyleSheet(
            "background-color:" + bg + ";"
            "border: 1px solid" + bg
        )
        self.home_bg = bg

    def stats_label(self, bg):
        self.stats = QPushButton(self)
        cgf.png_button(self.stats, "stats", self.iconSize)
        self.stats.move(
            int(self.spacing), 
            int(self.home.y() + self.home.height() + self.spacing)
        )
        self.stats.setStyleSheet(
            "background-color:" + bg + ";"
            "border: 1px solid" + bg
        )
        self.stats_bg = bg

    '''
    Menu
    
    '''
    def menu(self, bg):
        self.menu_widgets = []
        
        self.menublock_label(bg)
        self.menu_widgets.append(self.menuBlock)

        self.home_label2(bg)
        self.menu_widgets.append(self.homeLabel)

        self.stats_label2(bg)
        self.menu_widgets.append(self.statsLabel)

        # signals
        self.homeLabel.clicked.connect(lambda: self.homeClicked())
        self.statsLabel.clicked.connect(lambda: self.statsClicked())
    
    def menublock_label(self, bg):
        self.menuBlock = QLabel(self)
        self.menuBlock.setGeometry(self.sideBarBlock.x()+self.sideBarBlock.width(),
                                    int(self.home.y()-self.home.height()/2), 
                                    int(self.sideBarBlock.width()*1.5), 
                                    int(self.stats.y()+self.stats.height()*2-self.home.y()))
        self.menuBlock.setStyleSheet(
            "background-color:" + bg + ";"
            "color: white"
        )
    
    def home_label2(self, bg):
        self.homeLabel = QPushButton("Home", self)
        self.homeLabel.setFont(QFont(self.fontStyle, int(self.menuBlock.height()*0.05)))
        self.homeLabel.setGeometry(self.menuBlock.x()+self.spacing,
                                    int((self.home.y()*2+self.home.height()-int(self.menuBlock.height()/3-self.spacing))/2), 
                                    int(self.menuBlock.width()-self.spacing*2), 
                                    int(self.menuBlock.height()/3-self.spacing))
        self.homeLabel.setStyleSheet(
            "background-color:" + self.theme2 + ";"
            "border: 1px solid" + self.theme2 + ";"
            "text-align: left;"
            "color: white"
        )

    def stats_label2(self, bg):
        self.statsLabel = QPushButton("Statistics", self)
        self.statsLabel.setFont(QFont(self.fontStyle, int(self.menuBlock.height()*0.05)))
        self.statsLabel.setGeometry(self.menuBlock.x()+self.spacing,
                                    int((self.stats.y()*2+self.stats.height()-int(self.menuBlock.height()/3-self.spacing))/2), 
                                    int(self.menuBlock.width()-self.spacing*2), 
                                    int(self.menuBlock.height()/3-self.spacing))
        self.statsLabel.setStyleSheet(
            "background-color:" + bg + ";"
            "border: 1px solid" + bg + ";"
            "text-align: left;"
            "color: white"
        )

    '''
    Home Page
    
    '''
    def homepage(self):
        self.homepage_widgets = []
        self.homepage_x = self.sideBarBlock.width()
        self.homepage_y = self.headerBlock.height()
        self.homepage_w = self.width-self.sideBarBlock.width()
        self.homepage_h = self.height-self.headerBlock.height()

        self.homepage_container = QWidget(self)
        self.homepage_container.setStyleSheet("Background: red")
        # self.homepage_container.move(self.homepage_x, self.homepage_y)
        self.homepage_container.setGeometry(self.homepage_x, 
                                        self.homepage_y,
                                        self.homepage_w,
                                        self.homepage_h)
        
        self.homepage_layout = QHBoxLayout(self.homepage_container)

        self.piechart_container = QWidget(self)
        self.piechart_container.setStyleSheet("background: white")
        self.homepage_layout.addWidget(self.piechart_container)
        self.homepage_widgets.append(self.piechart_container)
        self.piechart_layout = QVBoxLayout(self.piechart_container)

        self.piecharttitle_label()
        self.piechart_layout.addWidget(self.pieChartTitle)
        self.homepage_widgets.append(self.pieChartTitle)

        self.piechart_label()
        self.piechart_layout.addWidget(self.pieChart)
        self.homepage_widgets.append(self.pieChart)        

        self.curr_ip = find_devices.get_current_ip()
        self.curr_hostname = find_devices.get_hostname(self.curr_ip)
        threading.Thread(target=self.update_pie_chart).start()
        # self.update_pie_chart()

        self.deviceinfoblock_label()
        self.deviceInfoBlock.hide()
        # self.homepage_widgets.append(self.deviceInfoBlock)

        self.deviceinfo_container = QWidget(self)
        self.deviceinfo_container.setStyleSheet("background: black")
        self.homepage_layout.addWidget(self.deviceinfo_container)
        self.homepage_widgets.append(self.deviceinfo_container)
        self.deviceinfo_layout = QVBoxLayout(self.deviceinfo_container)

        self.deviceinfotitle_label()
        self.deviceinfo_layout.addWidget(self.deviceInfoTitle)
        self.homepage_widgets.append(self.deviceInfoTitle)

        self.deviceip_label()
        self.deviceinfo_layout.addWidget(self.deviceIP)
        self.homepage_widgets.append(self.deviceIP)

        self.deviceipvalue_label()
        self.deviceinfo_layout.addWidget(self.deviceIPValue)
        self.homepage_widgets.append(self.deviceIPValue)

        self.devicename_label()
        self.deviceinfo_layout.addWidget(self.deviceName)
        self.homepage_widgets.append(self.deviceName)

        self.devicenamevalue_label()
        self.deviceinfo_layout.addWidget(self.deviceNameValue)
        self.homepage_widgets.append(self.deviceNameValue)
    
    def piecharttitle_label(self):
        self.pieChartTitle = QLabel("Devices on Your Network", self.homepage_container)
        self.pieChartTitle.setFont(QFont(self.fontStyle, int(self.homepage_h/8*0.15)))
        self.pieChartTitle.resize(QSize(int(self.homepage_w*0.7),
                                    int(self.homepage_h*0.1)))
        # self.pieChartTitle.setGeometry(self.homepage_x+self.spacing,
        #                             self.homepage_y+self.spacing,
        #                             int(self.pieChart.width()-self.spacing),
        #                             int(self.homepage_h/8*0.35))
        
        self.pieChartTitle.setStyleSheet(
            "background: white;"
            "border: 1px solid white;"
            "color:"+self.colorDarkBlue
        )

    def piechart_label(self):
        self.pieChart = QLabel(self.homepage_container)
        self.pieChart.resize(QSize(int(self.homepage_w*0.7), 
                                   int(self.homepage_h*0.7)))
        
        # self.pieChart.setGeometry(self.homepage_x, self.homepage_y,
        #                           int(self.homepage_h * 0.8*4/3), int(self.homepage_h*0.8))
        self.display_loading_img()

    def deviceinfoblock_label(self):
        self.deviceInfoBlock = QLabel(self.homepage_container)
        self.deviceInfoBlock.setGeometry(self.homepage_x+self.pieChart.width()+self.spacing,
                                    self.homepage_y,
                                    self.homepage_w-self.spacing-self.pieChart.width(),
                                    self.homepage_h)
        self.deviceInfoBlock.setStyleSheet(
            "background:"+self.colorDarkGrey+";"
            "border: 1px solid "+self.colorDarkGrey+";"
            "color: white"
        )

    def deviceinfotitle_label(self):
        self.deviceInfoTitle = QLabel("Device Information", self.homepage_container)
        self.deviceInfoTitle.setFont(QFont(self.fontStyle, int(self.homepage_h/8*0.15)))
        self.deviceinfo_container.resize(QSize(self.homepage_w-self.spacing-self.pieChart.width(),
                                    int(self.homepage_h/8*0.35)))
        # self.deviceInfoTitle.setGeometry(self.homepage_x+self.pieChart.width()+self.spacing,
        #                             self.homepage_y+self.spacing,
        #                             self.homepage_w-self.spacing-self.pieChart.width(),
        #                             int(self.homepage_h/8*0.35))
        self.deviceInfoTitle.setStyleSheet(
            "background:"+self.colorDarkGrey+";"
            "border: 1px solid "+self.colorDarkGrey+";"
            "color: white"
        )

    def deviceip_label(self):
        self.deviceIP = QLabel("IPv4 Address:", self.homepage_container)
        self.deviceIP.setFont(QFont(self.fontStyle, int(self.homepage_h/8*0.12)))
        self.deviceIP.setAlignment(Qt.AlignLeft)
        self.deviceIP.resize(QSize(int((self.deviceInfoBlock.width()-self.spacing*2)/2),
                                    int(self.homepage_h/8*0.35)))
        # self.deviceIP.setGeometry(self.homepage_x+self.pieChart.width()+self.spacing,
        #                             self.deviceInfoTitle.y()+self.deviceInfoTitle.height()+self.spacing,
        #                             int((self.deviceInfoBlock.width()-self.spacing*2)/2),
        #                             int(self.homepage_h/8*0.35))
        self.deviceIP.setStyleSheet(
            "background:"+self.colorDarkGrey+";"
            "border: 1px solid "+self.colorDarkGrey+";"
            "color: white"
        )

    def deviceipvalue_label(self):
        self.deviceIPValue = QLabel(self.curr_ip, self)
        self.deviceIPValue.setFont(QFont(self.fontStyle, int(self.homepage_h/8*0.12)))
        self.deviceIPValue.setAlignment(Qt.AlignLeft)
        self.deviceIPValue.resize(QSize(int((self.deviceInfoBlock.width()-self.spacing*2)/2),
                                    int(self.homepage_h/8*0.35)))
        # self.deviceIPValue.setGeometry(self.deviceIP.x()+self.deviceIP.width(),
        #                             self.deviceInfoTitle.y()+self.deviceInfoTitle.height()+self.spacing,
        #                             int((self.deviceInfoBlock.width()-self.spacing*2)/2),
        #                             int(self.homepage_h/8*0.35))
        self.deviceIPValue.setStyleSheet(
            "background:"+self.colorDarkGrey+";"
            "border: 1px solid "+self.colorDarkGrey+";"
            "color: white"
        )

    def devicename_label(self):
        self.deviceName = QLabel("Host Name:", self)
        self.deviceName.setFont(QFont(self.fontStyle, int(self.homepage_h/8*0.12)))
        self.deviceName.setAlignment(Qt.AlignLeft)
        self.deviceName.resize(QSize(int((self.deviceInfoBlock.width()-self.spacing*2)/2),
                                    int(self.homepage_h/8*0.35)))
        # self.deviceName.setGeometry(self.homepage_x+self.pieChart.width()+self.spacing,
        #                             self.deviceIP.y()+self.deviceIP.height()+self.spacing,
        #                             int((self.deviceInfoBlock.width()-self.spacing*2)/2),
        #                             int(self.homepage_h/8*0.35))
        self.deviceName.setStyleSheet(
            "background:"+self.colorDarkGrey+";"
            "border: 1px solid "+self.colorDarkGrey+";"
            "color: white"
        )
    
    def devicenamevalue_label(self):
        self.deviceNameValue = QLabel(self.curr_hostname, self)
        self.deviceNameValue.setFont(QFont(self.fontStyle, int(self.homepage_h/8*0.12)))
        self.deviceNameValue.setAlignment(Qt.AlignLeft)
        self.deviceNameValue.resize(QSize(int((self.deviceInfoBlock.width()-self.spacing*2)/2),
                                    int(self.homepage_h/8*0.35)))
        # self.deviceNameValue.setGeometry(self.deviceName.x()+self.deviceName.width()+self.spacing,
        #                             self.deviceIP.y()+self.deviceIP.height()+self.spacing,
        #                             int((self.deviceInfoBlock.width()-self.spacing*2)/2),
        #                             int(self.homepage_h/8*0.35))
        self.deviceNameValue.setStyleSheet(
            "background:"+self.colorDarkGrey+";"
            "border: 1px solid "+self.colorDarkGrey+";"
            "color: white"
        )
    
    '''
    Stats Page
    
    '''
    def statspage(self):
        return

    '''
    Test
    
    '''
    def menu_styling(self, color):
        points = [(self.menuBlock.x(), self.menuBlock.y()),
                  (self.menuBlock.x()+self.menuBlock.width(), self.sideBar.y()),
                  (self.menuBlock.x()+self.menuBlock.width(), self.sideBar.y())]

        print(points)
        # points = [(103, 160),
        #           (257, 160),
        #           (103, 111)]
        self.upperTriangle = PolygonWidget(points=points, parent=self)
        
        self.upperTriangle.setGeometry(self.menuBlock.x(), 
                                       self.sideBar.y(),
                                       self.menuBlock.width()-self.spacing,
                                       self.menuBlock.y()-self.sideBar.y()-self.spacing)
        # self.upperTriangle.setGeometry(103, 160, 
        #                                50, 
        #                                150)
        self.upperTriangle.hide()
        self.menu_widgets.append(self.upperTriangle)
        # self.menu_widgets.append(self.upperTriangle)

        points = [
        (50, 50),
        (150, 50),
        (150, 150)
        ]
        self.aTriangle = PolygonWidget(points=points, outline=Qt.red, color=Qt.red, parent=self)
        self.aTriangle.setGeometry(250, 250, 200, 200)
        self.aTriangle.hide()
        
        self.devices = []
        self.aButton = QPushButton("push", self)
        self.aButton.setStyleSheet("background:white; color:black;border:1px solid red")
        self.aButton.move(int(self.width/2), int(self.height/2))
        self.aButton.hide()

        self.aButton.clicked.connect(lambda: self.showTriangle())
    
    '''
    Signals
    
    '''
    def gearClicked(self):
        if self.settings_bg != self.colorDarkGrey:
            self.theme1 = self.colorBlack
            self.theme2 = self.colorDarkGrey

        elif self.settings_bg != self.colorDarkOrange:
            self.theme1 = self.colorOrange
            self.theme2 = self.colorDarkOrange

        self.settings_bg = self.theme2    
        self.settings.setStyleSheet(
            "background-color:" + self.theme2 + ";"
            "border: 1px solid" + self.theme2
            )
        
        for widgets in self.header_widgets:
            widgets.setStyleSheet(
            "background-color:" + self.theme1 + ";"
            "border: 1px solid" + self.theme1 + ";"
            "color: white"
            )
        for widgets in self.sidebar_widgets:
            widgets.setStyleSheet(
            "background-color:" + self.theme1 + ";"
            "border: 1px solid" + self.theme1 + ";"
            "color: white"
            )

        for widgets in self.menu_widgets:
            widgets.setStyleSheet(
            "background-color:" + self.theme1 + ";"
            "border: 1px solid" + self.theme1 + ";"
            "color: white"
            )
            
        self.homeClicked()

    def hamburgerClicked(self):
        if self.sideBar_bg != self.theme1:
            self.sideBar.setStyleSheet(
            "background-color:" + self.theme1 + ";"
            "border: 1px solid" + self.theme1
            )
            self.sideBar_bg = self.theme1
            # for widget in self.menu_widgets:
            #     widget.show()
            #     try:
            #         if widget.isVisible():
            #             widget.hide()
            #         else:
            #             widget.show()
            #     except:
            #         pass
        
        else:
            self.sideBar.setStyleSheet(
            "background-color:" + self.theme2 + ";"
            "border: 1px solid" + self.theme2
            )
            self.sideBar_bg = self.theme2
            # for widget in self.menu_widgets:
            #     print(widget)
            #     widget.hide()
            #     try:
            #         if widget.isVisible():
            #             print(widget, "hidden")
            #             widget.hide()
            #         else:
            #             print(widget, "shown")
            #             widget.show()
            #     except:
            #         pass
        for widget in self.menu_widgets:
                try:
                    if widget.isVisible():
                        widget.hide()
                    else:
                        widget.show()
                except:
                    pass

    def homeClicked(self):
        if self.home_bg != self.theme2:
            self.home.setStyleSheet(
            "background-color:" + self.theme2 + ";"
            "border: 1px solid" + self.theme2 + ";"
            "color: white"
            )
            try:
                self.homeLabel.setStyleSheet(
                "background-color:" + self.theme2 + ";"
                "border: 1px solid" + self.theme2 + ";"
                "text-align: left;"
                "color: white"
                )
            except:
                pass
            self.home_bg = self.theme2

            self.stats.setStyleSheet(
            "background-color:" + self.theme1 + ";"
            "border: 1px solid" + self.theme1 + ";"
            "color: white"
            )
            try:
                self.statsLabel.setStyleSheet(
                "background-color:" + self.theme1 + ";"
                "border: 1px solid" + self.theme1 + ";"
                "text-align: left;"
                "color: white"
                )
            except:
                pass
            self.stats_bg = self.theme1
            try:
                for widget in self.homepage_widgets:
                    widget.show()
            except:
                pass

    def statsClicked(self):
        if self.stats_bg != self.theme2:
            self.stats.setStyleSheet(
            "background-color:" + self.theme2 + ";"
            "border: 1px solid" + self.theme2 + ";"
            "color: white"
            )
            try:
                self.statsLabel.setStyleSheet(
                "background-color:" + self.theme2 + ";"
                "border: 1px solid" + self.theme2 + ";"
                "text-align: left;"
                "color: white"
                )
            except:
                pass
            self.stats_bg = self.theme2

            self.home.setStyleSheet(
            "background-color:" + self.theme1 + ";"
            "border: 1px solid" + self.theme1 + ";"
            "color: white"
            )
            try: self.homeLabel.setStyleSheet(
                "background-color:" + self.theme1 + ";"
                "border: 1px solid" + self.theme1 + ";"
                "text-align: left;"
                "color: white"
                )
            except:
                pass
            self.home_bg = self.theme1
            try:
                for widget in self.homepage_widgets:
                    widget.hide()
            except:
                pass

    def display_loading_img(self):
        loading_path = os.path.abspath("gui/images/loading.gif")
        self.loading = QMovie(loading_path)
        self.loading.setScaledSize(QSize(self.pieChart.width(),
                                  self.pieChart.height()))
        # self.loading.setScaledSize(QSize(int(self.homepage_h*0.8), int(self.homepage_h*0.8)))
        self.pieChart = QLabel(self)
        self.pieChart.setMovie(self.loading)
        # self.pieChart.setGeometry(self.homepage_x+self.spacing, self.homepage_y+self.spacing,
        #                           int(self.homepage_h*0.8*4/3),
        #                           int(self.homepage_h*0.8))
        self.loading.start()

    def update_pie_chart(self):
        self.devices = find_devices.scan_network(self.curr_ip)
        self.aButton.click()

        cgf.png_label(self.pieChart, "devices_pie", int(self.homepage_h*0.8))
        
    def showTriangle(self):
            if self.upperTriangle.isVisible():
                print("vis", self.upperTriangle.isVisible())
                # self.upperTriangle2.setVisible(False)
                # self.upperTriangle2.show()
                self.upperTriangle.hide()
                self.aTriangle.hide()
                 
            else:
                print("invis", self.upperTriangle.isVisible())
                # self.upperTriangle2.setVisible(True) 
                self.upperTriangle.show()
                self.upperTriangle.setGeometry(self.aButton.x(), self.aButton.y()+self.aButton.height()+self.spacing,
                                               30, 30)
                self.aTriangle.setGeometry(self.aButton.x(), self.aButton.y()+self.aButton.height()+self.spacing,
                                               30, 30)
                self.aTriangle.show()

            try:
                num_slices = len(self.devices)
                try:
                    span_angle = int(360/num_slices)
                except:
                    span_angle = 360
                curr_angle = 0
                self.pie_slices = {}
                for device in self.devices:
                    device_name = device["hostname"]
                    self.pie_slices[device_name] = piewidget.PieWidget(start_angle=curr_angle, span_angle=span_angle, outline=Qt.black, parent=self)
                    self.pie_slices[device_name].setGeometry(self.aButton.x()+self.aButton.width(), self.aButton.y()+self.aButton.height(),
                                                            100, 100)
                    self.pie_slices[device_name].show()
                    curr_angle+=span_angle
            except:
                pass

    def set_data(self, new_data):
        """Set new data and update the pie chart."""
        self.data = new_data
        self.update_pie_chart()