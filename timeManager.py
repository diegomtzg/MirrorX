import time
import smartMirrorManager
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DateAndTime(QWidget):
    global ticker

    def __init__(self):
        super(DateAndTime, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', smartMirrorManager.large_fontsize)
        font2 = QFont('Helvetica', smartMirrorManager.xlarge_fontsize)

        self.vbox = QVBoxLayout()
        self.time = ''
        self.timeLabel = QLabel()
        self.vbox.setAlignment(Qt.AlignRight)
        self.timeLabel.setAlignment(Qt.AlignRight)
        self.timeLabel.setFont(font2)
        self.timeLabel.setText("<font color='white'>temp time</font>")

        self.weekday = ''
        self.weekdayLabel = QLabel()
        self.weekdayLabel.setFont(font1)
        self.weekdayLabel.setAlignment(Qt.AlignRight)

        self.date = ''
        self.dateLabel = QLabel()
        self.dateLabel.setAlignment(Qt.AlignRight)
        self.dateLabel.setFont(font1)

        self.vbox.addWidget(self.timeLabel)
        self.vbox.addWidget(self.weekdayLabel)
        self.vbox.addWidget(self.dateLabel)

        self.vbox.addStretch(2)
        self.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)

         self.updateTime()

    def updateTime(self):
        global ticker

        timer = QTimer(self) # Timer class updates things every once in a while
        timer.timeout.connect(self.tick) # Connect timer to ticking method
        timer.start(1000) # Call every second
        ticker = False

    def tick(self):
        global ticker

        # Make ticker flash in clock
        if(ticker):
            newTime = time.strftime("%I:%M %p")  # ex. hour: 2:45 PM
            newTime = newTime.lstrip('0') # Remove leading zero from time
            ticker = False
        else:
            newTime = time.strftime("%I %M %p")  # ex. hour: 2:45 PM
            newTime = newTime.lstrip('0')  # Remove leading zero from time
            ticker = True

        newDayOfWeek = time.strftime("%A")
        tempMonth = time.strftime("%b")
        tempDate = time.strftime("%d").lstrip('0') # Remove leading zero from date
        tempYear = time.strftime("%Y")
        newDate = tempMonth + " " + tempDate + ", " + tempYear

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
