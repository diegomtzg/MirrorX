import weatherManager
import timeManager

import sys
import locale
import time
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

# Constants
small_fontsize = 12
med_fontsize = 18
large_fontsize = 28
xlarge_fontsize = 48
ui_locale = ''
time_format = 12
date_format = "%b %d, %Y"


def main():
    smartMirror_app = QApplication(sys.argv) # Create application (runnable from command line)
    window = mainUI() # Create application window
    sys.exit(smartMirror_app.exec_()) # Ensure clean app exit


class mainUI:
    def __init__(self):
        self.qt = QWidget()

        # Initialize application window's UI
        self.initUI()


    def initUI(self):
        # Make background dark
        self.darkPalette = QPalette()
        # self.darkPalette.setColor(QPalette.Foreground, Qt.white)
        self.darkPalette.setColor(QPalette.Background, Qt.black)
        self.qt.setPalette(self.darkPalette)

        # Add weather box
        self.qt.weather = weatherManager.Weather()
        self.qt.weather.setFixedHeight(150)
        self.qt.hbox1 = QHBoxLayout() # Horizontal relative layout
        self.qt.hbox1.addWidget(self.qt.weather)

        self.qt.setLayout(self.qt.hbox1)
        self.qt.showFullScreen()


if __name__ == '__main__':
    main()