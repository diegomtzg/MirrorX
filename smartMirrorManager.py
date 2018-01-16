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


class mainUI(QMainWindow):

    def __init__(self):
        # Initialize parent window object
        super(mainUI, self).__init__()

        # Initialize application window's UI
        self.initUI()


    def initUI(self):
        # Create full screen application window
        self.showFullScreen()
        self.setWindowTitle("magicMirror")

        # Make background dark
        darkPalette = QPalette()
        darkPalette.setColor(QPalette.Background, Qt.black)
        darkPalette.setColor(QPalette.Foreground, Qt.white)
        self.setPalette(darkPalette)

        self.hbox1 = QHBoxLayout()
        self.clock = DateAndTime()
        self.clock.setFixedHeight(150)

        self.hbox1.addWidget(self.clock)


class DateAndTime(QWidget):
    def __init__(self):
        super(DateAndTime, self).__init__()
        self.initUI()


    def initUI(self):
        font1 = QFont('Helvetica', large_fontsize)
        font2 = QFont('Helvetica', small_fontsize)

        # vbox = QVBoxLayout()
        # timeLabel = QLabel()
        # timeLabel.setAlignment(Qt.AlignRight)
        # timeLabel.setFont(font1)
        # vbox.addWidget(timeLabel)


        # Get current date
        # date = QDate.currentDate()
        # dateText = date.toString()

        # Get weekday name
        # weekdayNum = QDate.dayOfWeek()
        # weekDay = QDate.longDayName(weekdayNum)

        # Get current time
        #time = QTime.currentTime()
        #timeText = time.toString('hh:mm:ss a')



def main():
    # Create application
    app = QApplication([])

    # Create application window
    window = mainUI()

    # Ensure a clean exit
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()