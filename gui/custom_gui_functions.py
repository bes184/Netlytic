import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

def place_right(target, dest, spacing=0):
        target.move(int(dest.width()+dest.x()+spacing),
                    dest.y())
    
def place_down(target, dest, spacing=25):
    target.move(dest.x(), 
                int(dest.height()+dest.y()+spacing))

def place_center(target, dest):
    target.move(int((dest.width()-target.width())/2+dest.x()), 
                int((dest.height()-target.height())/2)+dest.y())

def center_horizontally(target, dest):
    target.move(int((dest.width()-target.width())/2+dest.x()), 
                target.y())

def png_label(label, icon_name, icon_size, input=0):
        if input == 0:
            icon_path = os.path.abspath(f"outputs/{icon_name}.jpeg")
        else:
            icon_path = os.path.abspath(f"gui/images/{icon_name}.png")
        pixmap = QtGui.QPixmap(icon_path)
        pixmap = pixmap.scaled(
            int(icon_size*4/3), icon_size
        )
        label.setPixmap(pixmap)
        label.resize(pixmap.size())

def png_button(button, icon_name, icon_size):
    icon_path = os.path.abspath(f"gui/images/{icon_name}.png")
    pixmap = QtGui.QPixmap(icon_path)
    pixmap = pixmap.scaled(
        icon_size, icon_size
    )
    button.setIcon(QtGui.QIcon(pixmap))
    button.setIconSize(pixmap.size())
    button.resize(pixmap.size())
    
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