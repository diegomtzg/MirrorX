import weatherManager
import timeManager
import quotesManager
import calendarManager

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

# TODO: Change welcome to good morning/afternoon based on time of day

# Constants
small_fontsize = 12
med_fontsize = 26
large_fontsize = 32
xlarge_fontsize = 70
global smartMirrorApp

PERSON_NAME = ""
PERSON_ID = ""
STARTED = False

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
        self.qt.quotesHBox = QHBoxLayout()
        self.qt.calendarHBox = QHBoxLayout()
        self.qt.welcomeHBox = QHBoxLayout()

        self.qt.verticalMirrorBox = QVBoxLayout()
        self.qt.verticalMirrorBox.addLayout(self.qt.weatherClockHBox)
        self.qt.verticalMirrorBox.addLayout(self.qt.calendarHBox)
        self.qt.verticalMirrorBox.addStretch(1)
        self.qt.verticalMirrorBox.addLayout(self.qt.welcomeHBox)
        self.qt.verticalMirrorBox.addLayout(self.qt.quotesHBox)

        self.qt.setLayout(self.qt.verticalMirrorBox)
        self.update_check()

    def update_check(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateWidgets)
        self.timer.start(1000)

    @staticmethod
    def clearLayout(layout):
        for i in reversed(range(layout.count())): 
            widget = layout.itemAt(i).widget()
            if widget != None:
                widget.deleteLater()

    def updateWidgets(self):
        global PERSON_NAME, PERSON_ID, STARTED
        if not STARTED and PERSON_NAME != "" and PERSON_ID != "":

            # Add clock/date and weather widgets
            self.qt.clock = timeManager.DateAndTime()
            self.qt.weather = weatherManager.Weather()
            self.qt.calendar = calendarManager.Calendar()

            self.qt.clock.setFixedHeight(300)
            self.qt.weather.setFixedSize(580, 300)

            # Add weather, calendar and clock widgets
            self.qt.weatherClockHBox.addWidget(self.qt.weather)
            self.qt.weatherClockHBox.addWidget(self.qt.clock)
            self.qt.calendarHBox.addWidget(self.qt.calendar)

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

            STARTED = True

        if STARTED and PERSON_NAME == "" and PERSON_ID == "":
            mainUI.clearLayout(self.qt.weatherClockHBox)
            mainUI.clearLayout(self.qt.calendarHBox)
            mainUI.clearLayout(self.qt.quotesHBox)
            mainUI.clearLayout(self.qt.welcomeHBox)

            STARTED = False


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
        # print('PHOTO SAVED')
        res = identifyPersonInImage(imgPath)
        print(res)
        if (len(res) == 1): # must only have one face
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
    while(num_count < 100):
        time.sleep(0.5)
        # cam.retrieve()
        success, image = cam.read()
        if not success: continue
        cv2.imwrite(imgPath, image)
        # print('PHOTO SAVED')
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
    import threading as T
    import cv2

    cam = cv2.VideoCapture(0) # TODO change to 1 for webcam
    imgPath = 'data/mostRecentFace.jpg'

    smartMirrorApp = QApplication(sys.argv)  # Create application (runnable from command line)
    window = mainUI()  # Create application window  
    T.Thread(target=initializeLogin).start()

    sys.exit(smartMirrorApp.exec_())  # Ensure clean app exit


