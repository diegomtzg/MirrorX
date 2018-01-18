from smartMirrorManager import *
import requests
import json
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *

small_fontsize = 20
med_fontsize = 30
large_fontsize = 40
xlarge_fontsize = 50

class Quotes(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(Quotes, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', small_fontsize)

        self.vbox = QVBoxLayout()
        self.lbl1 = QLabel()
        self.lbl2 = QLabel()
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.lbl2.setAlignment(Qt.AlignCenter)
        self.vbox.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.lbl1)
        self.vbox.addWidget(self.lbl2)
        self.lbl1.setFont(font1)
        self.lbl2.setFont(font1)
        self.setLayout(self.vbox)
        self.quotes_get()

    def quotes_get(self):
        try:
            url = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
            res = requests.get(url)
            s = res.text
            s.replace('\r\n', '')
            s.replace("\'", "'")
            data = json.loads(s)
            tempQuote = "<font color='white'>" + data["quoteText"] + "</font>"
            tempAuthor = temp = "<font color='white'>-" + data["quoteAuthor"] + "</font>"
            self.lbl1.setText(tempQuote)
            self.lbl2.setText(tempAuthor)

        except IOError:
            print('no internet')