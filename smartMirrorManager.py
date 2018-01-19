import weatherManager
import timeManager
import quotesManager
from audio_engine import *

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

# Constants
small_fontsize = 15
med_fontsize = 25
large_fontsize = 35
xlarge_fontsize = 45
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

        self.qt.hbox1 = QHBoxLayout() # Horizontal relative layout
        self.qt.hbox2 = QHBoxLayout()
        self.qt.welcomeBox = QHBoxLayout()

        self.qt.vbox = QVBoxLayout()
        self.qt.vbox.addLayout(self.qt.hbox1)
        self.qt.vbox.addStretch(1)
        self.qt.vbox.addLayout(self.qt.welcomeBox)
        #self.qt.vbox.addStretch(0.25)
        self.qt.vbox.addLayout(self.qt.hbox2)

        self.qt.setLayout(self.qt.vbox)
        self.update_check()

    def update_check(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateWidgets)
        self.timer.start(1000)

    @staticmethod
    def clearLayout(layout):
        print(layout.count())
        for i in reversed(range(layout.count())): 
            widget = layout.itemAt(i).widget()
            if widget != None:
                print(widget)
                #print(widget.parent())
                widget.deleteLater()

    def updateWidgets(self):
        global PERSON_NAME, PERSON_ID, STARTED
        if not STARTED and PERSON_NAME != "" and PERSON_ID != "":

            # Add clock/date and weather widgets
            self.qt.clock = timeManager.DateAndTime()
            self.qt.weather = weatherManager.Weather()

            self.qt.clock.setFixedHeight(150)
            self.qt.weather.setFixedHeight(150)

            # Add weather and clock widgets
            self.qt.hbox1.addWidget(self.qt.weather)
            self.qt.hbox1.addWidget(self.qt.clock)

            # Add welcome message
            font = QFont('Helvetica', med_fontsize)
            self.message = QLabel()
            self.message.setAlignment(Qt.AlignCenter)
            self.message.setFont(font)
            self.qt.welcomeBox.addWidget(self.message)
            self.message.setText("<font color='white'>" + "Welcome, " + PERSON_NAME + "</font>")

            # Add quotes widget
            self.qt.quotes = quotesManager.Quotes(QWidget())
            self.qt.hbox2.addWidget(self.qt.quotes)

            STARTED = True

        if STARTED and PERSON_NAME == "" and PERSON_ID == "":
            mainUI.clearLayout(self.qt.hbox1)
            mainUI.clearLayout(self.qt.hbox2)
            mainUI.clearLayout(self.qt.welcomeBox)

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
        print("a")
        success, image = cam.read()
        if not success: continue
        print("b")
        cv2.imwrite(imgPath, image)
        print("c")
        res = identifyPersonInImage(imgPath)
        print('d')
        if (len(res) == 1): # must only have one face
            name = getPerson(res[0])
            print("Identified %s" % name['name'])
            break
        print("e")

    PERSON_NAME = name['name']
    PERSON_ID = res[0]

    time.sleep(2)
    personWav = "voiceCommands/welcome_" + PERSON_NAME.lower() + ".wav"
    play(personWav)

    faceGoneAndRestart()

def faceGoneAndRestart():
    from facial_recognition import identifyPersonInImage, getPerson
    import time

    global PERSON_NAME, PERSON_ID, cam, imgPath

    num_count = 0
    # stop in 10 seconds
    while(num_count < 5):
        time.sleep(0.5)
        print("A")
        cam.retrieve()
        success, image = cam.read()
        if not success: continue
        print("B")
        cv2.imwrite(imgPath, image)
        print("C")
        res = identifyPersonInImage(imgPath)
        print("D")
        if (len(res) == 0 or PERSON_ID not in res): # must only have one face
            print("Identified no face! Count %d " % num_count)
            num_count += 1
        else:
            print("Identified %s with ID %s" % (PERSON_NAME, PERSON_ID))
            num_count = 0
        print('E')

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

    cam = cv2.VideoCapture(0)
    imgPath = 'data/mostRecentFace.jpg'

    smartMirrorApp = QApplication(sys.argv)  # Create application (runnable from command line)
    window = mainUI()  # Create application window  
    T.Thread(target=initializeLogin).start()

    sys.exit(smartMirrorApp.exec_())  # Ensure clean app exit


