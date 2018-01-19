import sys
import locale
import time
from smartMirrorManager import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

# Constants
small_fontsize = 15
med_fontsize = 25
large_fontsize = 35
xlarge_fontsize = 45

class DateAndTime(QWidget):
    def __init__(self):
        super(DateAndTime, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', xlarge_fontsize)
        font2 = QFont('Helvetica', med_fontsize)

        self.vbox = QVBoxLayout()
        self.time = ''
        self.timeLabel = QLabel()
        self.vbox.setAlignment(Qt.AlignRight)
        self.timeLabel.setFont(font1)
        self.timeLabel.setText("<font color='white'>temp time</font>")

        self.weekday = ''
        self.weekdayLabel = QLabel()
        self.weekdayLabel.setFont(font2)
        self.weekdayLabel.setAlignment(Qt.AlignRight)

        self.date = ''
        self.dateLabel = QLabel()
        self.dateLabel.setAlignment(Qt.AlignRight)
        self.dateLabel.setFont(font2)

        self.vbox.addWidget(self.timeLabel)
        self.vbox.addStretch(0.5)
        self.vbox.addWidget(self.weekdayLabel)
        self.vbox.addWidget(self.dateLabel)

        self.vbox.addStretch(2)
        self.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
        self.updateTime()

    def updateTime(self):
        timer = QTimer(self) # Timer class updates things every once in a while
        timer.timeout.connect(self.tick) # Connect timer to ticking method
        timer.start(200) # Call every 200 ms

    def tick(self):
        newTime = time.strftime("%I:%M %p") # ex. hour: 2:45 PM
        newDayOfWeek = time.strftime("%A")
        newDate = time.strftime("%b %d, %Y")

        if newTime != self.time:
            temp = "<font color='white'>" + newTime + "</font>"
            self.time = newTime
            self.timeLabel.setText(temp)

        if newDayOfWeek != self.weekday:
            temp = "<font color='white'>" + newDayOfWeek + "</font>"
            self.weekday = newDayOfWeek
            self.weekdayLabel.setText(temp)

        if newDate != self.date:
            temp = "<font color='white'>" + newDate + "</font>"
            self.date = newDate
            self.dateLabel.setText(temp)
