import calendarManager
import weatherManager
import timeManager
import quotesManager
import newsManager

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

# Constants
small_fontsize = 12
med_fontsize = 26
large_fontsize = 32
xlarge_fontsize = 70
title_fontsize = 40

global smartMirrorApp

PERSON_NAME = "Diego"

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

        calendarManager.CLIENT_SECRET_FILE = "json_files/" + PERSON_NAME + ".json"

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
        dummyLabel.setFixedWidth(350)

        # Add weather, calendar and clock widgets
        self.qt.weatherClockHBox.addWidget(self.qt.weather)
        self.qt.weatherClockHBox.addWidget(self.qt.clock)
        self.qt.calendarNewsHBox.addWidget(self.qt.news)
        self.qt.calendarNewsHBox.addWidget(dummyLabel)  # For spacing
        self.qt.calendarNewsHBox.addWidget(self.qt.calendar)

        # Add welcome message
        font = QFont('Helvetica', xlarge_fontsize)
        self.message = QLabel()
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setFont(font)
        self.qt.welcomeHBox.addWidget(self.message)
        self.message.setText("<font color='white'>" + "Welcome, " + PERSON_NAME + "</font>")

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


def waitToScanFace(MAGIC_PHRASE):
    import speech_recognition as sr
    r = sr.Recognizer() # obtain audio from the microphone
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source, duration=2)
        while(True):
            try:
                audio = r.listen(source, phrase_time_limit=10)
                recognized = r.recognize_google(audio).lower()
                print(recognized)
                if MAGIC_PHRASE.lower() in recognized:
                    break
            except sr.UnknownValueError:
                print("Google failed to recognize")
            except sr.WaitTimeoutError:
                print("Re-listening due to time limit")
        print("Success! Magic phrase recognized")


def findFaceAndSetName():
    from facial_recognition import identifyPersonInImage, getPerson
    import time

    global PERSON_NAME, PERSON_ID, cam, imgPath

    while(True):
        time.sleep(0.5)
        success, image = cam.read()
        if not success: continue
        cv2.imwrite(imgPath, image)
        res = identifyPersonInImage(imgPath)
        print(res)
        if (len(res) == 1): # Must only have one face
            name = getPerson(res[0])
            print("Identified %s" % name['name'])
            break

    PERSON_NAME = name['name']
    PERSON_ID = res[0]

    faceGoneAndRestart()

def faceGoneAndRestart():
    from facial_recognition import identifyPersonInImage, getPerson
    import time

    global PERSON_NAME, PERSON_ID, cam, imgPath

    num_count = 0
    while(num_count < 10):
        time.sleep(0.5)
        success, image = cam.read()
        if not success: continue
        cv2.imwrite(imgPath, image)
        res = identifyPersonInImage(imgPath)
        if (len(res) == 0 or PERSON_ID not in res): # must only have one face
            print("Identified no face of %s! Count %d " % (PERSON_NAME, num_count))
            num_count += 1
        else:
            print("Identified %s with ID %s" % (PERSON_NAME, PERSON_ID))
            num_count = 0

    PERSON_NAME = ""
    PERSON_ID = ""

    time.sleep(2)
    findFaceAndSetName()


def initializeLogin():
    # waitToScanFace("mirror")
    findFaceAndSetName()


def start_qt():
    global smartMirrorApp
    smartMirrorApp = QApplication(sys.argv)  # Create application (runnable from command line)
    window = mainUI()  # Create application window 

if __name__ == '__main__':
    import cv2

    smartMirrorApp = QApplication(sys.argv)  # Create application (runnable from command line)
    window = mainUI()  # Create application window  

    sys.exit(smartMirrorApp.exec_())  # Ensure clean app exit


