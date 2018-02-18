import calendarManager
import weatherManager
import timeManager
import quotesManager
import newsManager

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

# Constants for desktop version
# small_fontsize = 12
# med_fontsize = 26
# large_fontsize = 32
# xlarge_fontsize = 70
# title_fontsize = 40

# Constants for Raspberry pi Version
small_fontsize = 10
med_fontsize = 20
large_fontsize = 26
xlarge_fontsize = 50
title_fontsize = 30

global smartMirrorApp
global timeOfDay

PERSON_NAME = ""

class mainUI():
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

        self.qt.weatherClockHBox = QHBoxLayout()
        self.qt.calendarNewsHBox = QHBoxLayout()
        self.qt.welcomeHBox = QHBoxLayout()
        self.qt.quotesHBox = QHBoxLayout()

        self.qt.verticalMirrorBox = QVBoxLayout()
        self.qt.verticalMirrorBox.addLayout(self.qt.weatherClockHBox)
        # self.qt.verticalMirrorBox.addStretch(10) Uncomment to make news and calendar go to bottom of mirror
        self.qt.verticalMirrorBox.addLayout(self.qt.calendarNewsHBox)
        self.qt.verticalMirrorBox.addStretch(1)
        self.qt.verticalMirrorBox.addLayout(self.qt.welcomeHBox)
        self.qt.verticalMirrorBox.addLayout(self.qt.quotesHBox)

        self.qt.setLayout(self.qt.verticalMirrorBox)
        self.addWidgets()

    @staticmethod
    def clearLayout(layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget != None:
                widget.deleteLater()

    def addWidgets(self):
            # Add clock/date and weather widgets
            self.qt.clock = timeManager.DateAndTime()
            self.qt.weather = weatherManager.Weather()
            self.qt.calendar = calendarManager.Calendar()
            self.qt.news = newsManager.News()

            self.qt.clock.setFixedHeight(300)
            self.qt.weather.setFixedSize(580, 300)
            self.qt.news.setFixedWidth(360)
            self.qt.calendar.setFixedWidth(300)

            dummyLabel = QLabel()
            dummyLabel.setFixedWidth(340)

            # Add weather, calendar and clock widgets
            self.qt.weatherClockHBox.addWidget(self.qt.weather)
            self.qt.weatherClockHBox.addWidget(self.qt.clock)
            self.qt.calendarNewsHBox.addWidget(self.qt.news)
            self.qt.calendarNewsHBox.addWidget(dummyLabel)  # For spacing
            self.qt.calendarNewsHBox.addWidget(self.qt.calendar)

            # Add welcome message
            message = ''
            font = QFont('Helvetica', xlarge_fontsize)
            self.message = QLabel()
            self.message.setAlignment(Qt.AlignCenter)
            self.message.setFont(font)
            self.qt.welcomeHBox.addWidget(self.message)

            if timeOfDay == "PM":
                message = "Good Morning, "
            elif timeOfDay == "AM":
                message = "Good Afternoon, "

            self.message.setText("<font color='white'>" + message + PERSON_NAME + "</font>")

            # Add quotes widget
            self.qt.quotes = quotesManager.Quotes(QWidget())
            self.qt.quotesHBox.addWidget(self.qt.quotes)


# idk how this all really works but hey at least we can quit the app by clicking 'q'
class QKeyFilter(QObject):
    qKeyPressed = pyqtSignal()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Q:
                cam.release()
                cv2.destroyAllWindows()
                sys.exit(smartMirrorApp.exec_())
        return False


def start_qt():
    global smartMirrorApp
    smartMirrorApp = QApplication(sys.argv)  # Create application (runnable from command line)
    window = mainUI()  # Create application window 

if __name__ == '__main__':
    import cv2

    smartMirrorApp = QApplication(sys.argv)  # Create application (runnable from command line)
    window = mainUI()  # Create application window

    sys.exit(smartMirrorApp.exec_())  # Ensure clean app exit


