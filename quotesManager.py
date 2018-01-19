from smartMirrorManager import *
import requests
import json
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import *
import numpy as np

small_fontsize = 15
med_fontsize = 25
large_fontsize = 35
xlarge_fontsize = 45

QUOTES =  [("Once we accept our limits, we go beyond them", 'Albert Einstein'),
          ("Carpe Diem", "David Kosbie"),
          ("Don't cry because it's over, smile because it happened", "Dr. Seuss"),
          ("Be yourself; everyone is already taken", "Oscar Wilde"),
          ("We cannot change the cards that we are dealt, just how we play the hand", "Randy Pausch"),
          ("The brick walls are there for a reason...", "Randy Pausch"),
          ("Luck is where preparation meets opportunity", "Randy Pausch"),
          ("Be the change you wish to see in the world", "Ghandi"),
          ("You only live once, but if you do it right once is enough", "Mae West"),
          ("Stay hungry, stay foolish", "Steve Jobs"),
          ("You cannot shake hands with a clenched fist", "Ghandi"),
          ("The only journey is the one within", "Rainer Rike"),
          ("Love cures people - both the ones who give it and the ones who receive it", "Karl A. Menninger")
]

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
            data = json.loads(s)
            quote = data["quoteText"]
            if len(quote) > 80:
                (quote, author) = QUOTES[np.random.randint(len(QUOTES))]

            tempQuote = "<font color='white'>" + quote + "</font>"
            author = data["quoteAuthor"]
            if len(author) < 2:
                author = "Unknown"
            tempAuthor = "<font color='white'>-" + author + "</font>"
            self.lbl1.setText(tempQuote)
            self.lbl2.setText(tempAuthor)

        except Exception as e:
            (quote, author) = QUOTES[np.random.randint(len(QUOTES))]
            self.lbl1.setText("<font color='white'>" + quote + "</font>")
            self.lbl2.setText("<font color='white'>-" + author + "</font>")

