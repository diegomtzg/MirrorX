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
global smartMirrorApp

class mainUI:
    def __init__(self):
        self.qt = QWidget()
        self.initUI()

    def initUI(self):
        self.qt.showFullScreen()

        #Install signal filter to receive 'q' clicks to be able to quit app
        filter = QKeyFilter(self.qt)
        self.qt.installEventFilter(filter)

        # Make background dark
        self.darkPalette = QPalette()
        # doesn't work self.darkPalette.setColor(QPalette.Foreground, Qt.white)
        self.darkPalette.setColor(QPalette.Background, Qt.black)
        self.qt.setPalette(self.darkPalette)

        # Add clock/date and weather widgets
        self.qt.clock = timeManager.DateAndTime()
        self.qt.weather = weatherManager.Weather()

        self.qt.clock.setFixedHeight(150)
        self.qt.weather.setFixedHeight(150)

        self.qt.hbox1 = QHBoxLayout() # Horizontal relative layout
        self.qt.hbox1.addWidget(self.qt.weather)
        self.qt.hbox1.addStretch()
        self.qt.hbox1.addWidget(self.qt.clock)

        self.qt.setLayout(self.qt.hbox1)

# idk how this all really works but hey at least we can quit the app by clicking 'q'
class QKeyFilter(QObject):
    qKeyPressed = pyqtSignal()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Q:
                sys.exit(smartMirrorApp.exec_())
        return False


if __name__ == '__main__':
    smartMirrorApp = QApplication(sys.argv)  # Create application (runnable from command line)
    window = mainUI()  # Create application window
    sys.exit(smartMirrorApp.exec_())  # Ensure clean app exit