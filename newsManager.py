import requests
import json
import smartMirrorManager

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'MirrorX'

NEWS_API_KEY = "3e115fc75b1744a685b212b8b66acf6a" # From newsapi.org
NEWS_SOURCE = "abc-news" # From https://newsapi.org/sources
MAX_HEADLINES = 6

class News(QWidget):
    def __init__(self):
        super(News, self).__init__()
        self.initUI()

    def initUI(self):
        self.titleFont = QFont('Helvetica', smartMirrorManager.title_fontsize)
        self.newsContentFont = QFont('Helvetica', smartMirrorManager.med_fontsize)

        self.newsTitleBox = QHBoxLayout()
        self.newsContentBox = QVBoxLayout() # News headlines + title

        self.newsTitle = QLabel("<font color='white'>Today's Headlines</font>")
        self.newsTitle.setFont(self.titleFont)
        self.newsTitle.setAlignment(Qt.AlignCenter)

        self.newsTitleBox.addWidget(self.newsTitle)
        self.newsContentBox.addLayout(self.newsTitleBox)

        self.newsRows = QFormLayout()
        self.newsRows.setVerticalSpacing(20)
        self.newsRows.setAlignment(Qt.AlignLeft)
        self.newsContentBox.addLayout(self.newsRows)

        self.setLayout(self.newsContentBox)

        self.getNews()
        self.updateNews()

    def updateNews(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getNews)
        self.timer.start(1000 * 60 * 10)  # Update news every 10 minutes

    def getNews(self):
        news_req_url = "https://newsapi.org/v2/top-headlines?sources=%s&apiKey=%s" % (NEWS_SOURCE, NEWS_API_KEY)
        response = requests.get(news_req_url)
        news_json = json.loads(response.text)

        j = 1
        for i in range(0, MAX_HEADLINES):
            headline = news_json['articles'][i]['title']

            # Skip long headlines
            while(len(headline) > 70):
                headline = news_json['articles'][i + j]['title']
                j = j+1

            if headline[-1] != '?':
                headline =  headline + "."

            newHeadline = QLabel("<font color='white'>• " + headline + "</font>")
            newHeadline.setWordWrap(QFormLayout.WrapAllRows)
            newHeadline.setAlignment(Qt.AlignJustify)
            newHeadline.setFont(self.newsContentFont)
            self.newsRows.addRow(newHeadline)