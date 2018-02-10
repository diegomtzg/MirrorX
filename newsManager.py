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
NEWS_SOURCE = "abc-news,the-wall-street-journal" # From https://newsapi.org/sources
MAX_HEADLINES = 8

class News(QWidget):
    def __init__(self):
        super(News, self).__init__()
        self.initUI()

    def initUI(self):
        self.titleFont = QFont('Helvetica', smartMirrorManager.title_fontsize)
        self.newsContentFont = QFont('Helvetica', 20)

        self.newsTitleBox = QHBoxLayout()
        self.newsContentBox = QVBoxLayout() # News headlines + title

        self.newsTitle = QLabel("<font color='white'>Today's Headlines</font>")
        self.newsTitle.setFont(self.titleFont)
        self.newsTitle.setAlignment(Qt.AlignJustify)

        self.newsTitleBox.addWidget(self.newsTitle)
        self.newsContentBox.addLayout(self.newsTitleBox)

        self.newsRows = QFormLayout()
        self.newsRows.setVerticalSpacing(30)
        self.newsRows.setAlignment(Qt.AlignLeft)
        self.newsContentBox.addLayout(self.newsRows)

        self.setLayout(self.newsContentBox)

        self.getNews()
        self.updateNews()

    def updateNews(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getNews)
        self.timer.start(1000 * 60 * 30)  # Update news every 30 minutes

    def getNews(self):
        # Remove current rows so that new rows don't get added to previous rows, but replace them instead
        self.newsRows.deleteLater()
        self.newsRows = QFormLayout()
        self.newsRows.setVerticalSpacing(30)
        self.newsRows.setAlignment(Qt.AlignLeft)
        self.newsContentBox.addLayout(self.newsRows)

        news_req_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=%s" % (NEWS_API_KEY)
        response = requests.get(news_req_url)
        news_json = json.loads(response.text)

        for i in range(0, MAX_HEADLINES):
            headline = news_json['articles'][i]['title']
            source = news_json['articles'][i]['source']['name']
            source = source.rstrip(".com")

            if headline[-1] != '?':
                headline =  headline + "."

            newHeadline = QLabel("<font color='white'>– " + source + ": \"" + headline + "\"</font>")
            newHeadline.setWordWrap(QFormLayout.WrapAllRows)
            newHeadline.setAlignment(Qt.AlignLeft)
            newHeadline.setFont(self.newsContentFont)
            self.newsRows.addRow(newHeadline)