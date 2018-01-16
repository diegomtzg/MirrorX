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
        # self.darkPalette.setColor(QPalette.Background, Qt.black)
        self.qt.setPalette(self.darkPalette)

        # Add weather
        self.qt.weather = Weather()
        self.qt.weather.setFixedHeight(150)
        self.qt.hbox1 = QHBoxLayout() # Horizontal relative layout
        self.qt.hbox1.addWidget(self.qt.weather)

        self.qt.setLayout(self.qt.hbox1)
        self.qt.showFullScreen()



class Weather(QWidget):
    def __init__(self):
        super(Weather, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', large_fontsize)
        self.vbox = QVBoxLayout()
        self.temperatureLbl = QLabel('Tepr')
        self.temperatureLbl.setFont(font1)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.temperatureLbl)
        self.setLayout(self.hbox)



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



if __name__ == '__main__':
    main()