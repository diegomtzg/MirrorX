import weatherManager
import timeManager
import quotesManager

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

# Constants
small_fontsize = 12
med_fontsize = 18
large_fontsize = 28
xlarge_fontsize = 48
global smartMirrorApp

class mainUI:
    def __init__(self, personId):
        self.qt = QWidget()
        self.initUI()
        self.personId = personId

        # connecting with signal
        self.connect(self, SIGNAL("noFace"), self.exit)
        thread = worker(personId)
        thread.start()

    def exit(self, sigmsg):
        print(sigmsg)
        sys.exit(smartMirrorApp.exec_())  # Ensure clean app exit


    def initUI(self):
        self.qt.showFullScreen()

        #Install signal filter to receive 'q' clicks to be able to quit app
        filter = QKeyFilter(self.qt)
        self.qt.installEventFilter(filter)

        # Make background dark
        self.darkPalette = QPalette()
        # doesn't work self.darkPalette.setColor(QPalette.Foreground, Qt.white)
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

        # Add quotes widget
        self.qt.hbox2 = QHBoxLayout()
        self.qt.quotes = quotesManager.Quotes(QWidget())
        self.qt.hbox2.addWidget(self.qt.quotes)

        self.qt.vbox = QVBoxLayout()
        self.qt.vbox.addLayout(self.qt.hbox1)
        self.qt.vbox.addStretch(1)
        self.qt.vbox.addLayout(self.qt.hbox2)

        self.qt.setLayout(self.qt.vbox)



# idk how this all really works but hey at least we can quit the app by clicking 'q'
class QKeyFilter(QObject):
    qKeyPressed = pyqtSignal()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Q:
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


class worker(QThread):
    def __init__(self, personId):
        QThread.__init__(self, parent=smartMirrorApp)
        self.signal = SIGNAL("noFace")
        self.personId = personId

    def run(self):
        import time
        missCount = 0
        cam = cv2.VideoCapture(1)
        imgPath = '/data/workerFace.jpg'
        while(missCount < 3):
            time.sleep(5)
            success, image = cam.read()
            if not success: continue
            cv2.imwrite(imgPath)
            res = identifyPersonInImage(imgPath)
            if self.personId in res:
                missCount = 0
            else:
                missCount += 1
        cv2.destroyAllWindows()
        self.emit(self.signal, "unable to detect face for 3 iterations")



if __name__ == '__main__':
    while(True):
        smartMirrorApp = QApplication(sys.argv)  # Create application (runnable from command line)
        # waitToScanFace("mirror")
        from facial_recognition import identifyPersonInImage
        import cognitive_face as CF
        import cv2
        # take a picture from raspberry pi
        cam = cv2.VideoCapture(0)
        imgPath = 'data/mostRecentFace.jpg'
        PERSON_GROUP_ID = 'mirror-pg'

        # stop in 10 seconds
        while(True):
            success, image = cam.read()
            if not success: continue
            cv2.imwrite(imgPath, image)
            print("Write success!")
            res = identifyPersonInImage(imgPath)
            print(res)
            if (len(res) == 1):
                name = CF.person.get(PERSON_GROUP_ID, res[0])
                print(name)
                break    # must only have one face
            # login to the faceId/start app
        cv2.destroyAllWindows()
        

        # create thread that takes a picture every 5 seconds, if the specific 
        # face disappears for 15 seconds, shut down application
        window = mainUI(res[0])  # Create application window
        
    sys.exit(smartMirrorApp.exec_())  # Ensure clean app exit



