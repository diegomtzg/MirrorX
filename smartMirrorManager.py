import weatherManager
import timeManager
import quotesManager

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

# Constants
small_fontsize = 20
med_fontsize = 30
large_fontsize = 40
xlarge_fontsize = 50
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

        # Add welcome text widget
        # self.qt.hbox3 = QHBoxLayout()
        # self.qt.hbox3.addWidget()


        # Add quotes widget
        self.qt.hbox2 = QHBoxLayout()
        self.qt.quotes = quotesManager.Quotes(QWidget())
        self.qt.hbox2.addWidget(self.qt.quotes)

        self.qt.vbox = QVBoxLayout()
        self.qt.vbox.addLayout(self.qt.hbox1)
        self.qt.vbox.addStretch(1)
        self.qt.vbox.addLayout(self.qt.hbox2)

        self.qt.setLayout(self.qt.vbox)

class WelcomeMessage(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(WelcomeMessage, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', small_fontsize)
        self.vbox = QVBoxLayout()
        self.lbl1 = QLabel()
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.vbox.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.lbl1)
        self.lbl1.setFont(font1)
        self.setLayout(self.vbox)
        temp = "<font color='white'>Welcome, person</font>"
        self.lbl1.setText(temp)


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