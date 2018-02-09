import smartMirrorManager
import requests
import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *
import numpy as np

QUOTES =  [("Once we accept our limits, we go beyond them.", 'Albert Einstein'),
          ("Don't cry because it's over, smile because it happened.", "Dr. Seuss"),
          ("Be yourself; everyone is already taken.", "Oscar Wilde"),
          ("We cannot change the cards that we are dealt, just how we play the hand.", "Randy Pausch"),
          ("Luck is where preparation meets opportunity.", "Randy Pausch"),
          ("Be the change you wish to see in the world.", "Ghandi"),
          ("You only live once, but if you do it right once is enough.", "Mae West"),
          ("Stay hungry, stay foolish.", "Steve Jobs"),
          ("You cannot shake hands with a clenched fist.", "Ghandi"),
          ("The only journey is the one within.", "Rainer Rike"),
          ("Love cures people - both the ones who give it and the ones who receive it.", "Karl A. Menninger")
]

class Quotes(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(Quotes, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', smartMirrorManager.med_fontsize)

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
        self.updateQuotes()

    def updateQuotes(self):
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.quotes_get)
            self.timer.start(1000 * 60 * 2)  # Update quote every 2 minutes

    def quotes_get(self):
        try:
            url = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
            res = requests.get(url)
            s = res.text
            data = json.loads(s)
            quote = data["quoteText"]
            author = data["quoteAuthor"]
            if len(author) < 2:
                author = "Unknown"

            if len(quote) > 80:
                (quote, author) = QUOTES[np.random.randint(len(QUOTES))]

            # Get rid of quotes and authors with weird characters in them
            for i in range (0, len(quote)):
                asciiVal = ord(quote[i])
                if(asciiVal > 126 or asciiVal < 32):
                    (quote, author) = QUOTES[np.random.randint(len(QUOTES))]

            for i in range(0, len(author)):
                asciiVal = ord(author[i])
                if (asciiVal > 126 or asciiVal < 32):
                    (quote, author) = QUOTES[np.random.randint(len(QUOTES))]

            # Get rid of all trailing white space and random quotes placed by shady quote API service
            quote = quote.replace("\" ", "")
            quote = quote.rstrip(" ")

            tempQuote = "<font color='white'>\"" + quote + "\"</font>"
            tempAuthor = "<font color='white'>-" + author + "</font>"
            self.lbl1.setText(tempQuote)
            self.lbl2.setText(tempAuthor)

        except Exception as e:
            (quote, author) = QUOTES[np.random.randint(len(QUOTES))]
            self.lbl1.setText("<font color='white'>\"" + quote + "\"</font>")
            self.lbl2.setText("<font color='white'>–" + author + "</font>")