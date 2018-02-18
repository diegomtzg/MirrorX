import smartMirrorManager
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *


class Message(QWidget):
    def __init__(self):
        super(Message, self).__init__()
        self.initUI()

    def initUI(self):
        message = ''
        font = QFont('Helvetica', smartMirrorManager.xlarge_fontsize)

        self.hbox = QHBoxLayout()
        self.message = QLabel()
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setFont(font)
        self.hbox.addWidget(self.message)

        self.getMessage()
        self.updateMessage()

    def updateMessage(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getMessage)
        self.timer.start(1000 * 60 * 0.01)  # Update message every tenth of a second (to get it correct at startup)

    def getMessage(self):
        if smartMirrorManager.timeOfDay == "pm":
            message = "Good Afternoon, " + smartMirrorManager.PERSON_NAME
        elif smartMirrorManager.timeOfDay == "am":
            message = "Good Morning, " + smartMirrorManager.PERSON_NAME

        self.message.setText("<font color='white'>" + message + "</font>")
        self.setLayout(self.hbox)