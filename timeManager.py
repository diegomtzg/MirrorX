import sys
import locale
import time
from smartMirrorManager import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

class DateAndTime(QWidget):
    def __init__(self):
        super(DateAndTime, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', large_fontsize)
        font2 = QFont('Helvetica', small_fontsize)

        self.vbox = QVBoxLayout()
        self.time = ''
        self.timeLabel = QLabel('')
        self.vbox.setAlignment(Qt.AlignRight)
        self.timeLabel.setFont(font1)
        self.vbox.addWidget(self.timeLabel)
        self.vbox.addStretch(2)
        self.vbox.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox)
        self.time_update()


        # Get current date
        # date = QDate.currentDate()
        # dateText = date.toString()

        # Get weekday name
        # weekdayNum = QDate.dayOfWeek()
        # weekDay = QDate.longDayName(weekdayNum)

        # Get current time
        #time = QTime.currentTime()
        #timeText = time.toString('hh:mm:ss a')

