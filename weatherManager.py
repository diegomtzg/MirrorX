import requests
import json
import smartMirrorManager
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

weather_api_token = '9435a4c25a087440d56cc46775e1eb0d'

font1 = QFont('Helvetica', smartMirrorManager.med_fontsize)
font2 = QFont('Helvetica', smartMirrorManager.med_fontsize)
font3 = QFont('Helvetica', smartMirrorManager.large_fontsize)

icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}

class Weather(QWidget):
    def __init__(self):
        super(Weather, self).__init__()
        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()

        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''

        self.tempLabel = QLabel()
        self.tempLabel.setFont(font3)
        self.tempLabel.setText("<font color='white'>temporary temp</font>")
        self.iconLabel = QLabel()
        self.currentlyLabel = QLabel()
        self.currentlyLabel.setFont(font2)
        self.currentlyLabel.setText("<font color='white'>temporary curr</font>")
        self.forecastLabel = QLabel()
        self.forecastLabel.setFont(font1)
        self.forecastLabel.setWordWrap(True)
        self.forecastLabel.setText("<font color='white'>temporary forecast</font>")
        self.locLabel = QLabel()
        self.locLabel.setFont(font1)
        self.locLabel.setText("<font color='white'>temporary loc</font>")

        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox1 = QVBoxLayout()
        self.hbox.addWidget(self.tempLabel)
        self.hbox.addWidget(self.iconLabel)
        self.hbox.setAlignment(Qt.AlignLeft)
        self.vbox1.addWidget(self.currentlyLabel)
        self.vbox1.addWidget(self.forecastLabel)
        self.vbox1.addWidget(self.locLabel)
        self.vbox1.addStretch(1)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.vbox1)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox)
        self.getWeather()
        self.updateWeather()

    def updateWeather(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getWeather)
        self.timer.start(150000) # Update weather every 2.5ish minutes

    def getIP(self):
        try:
            # Fetch IP from jsonip.com and parse returned JSON
            ip_url = "http://jsonip.com"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            return "Error %s. Cannot get ip." % e

    def getWeather(self):
        try:
            loc_req_url = "http://freegeoip.net/json/%s" % self.getIP()
            req = requests.get(loc_req_url)
            loc_json = json.loads(req.text)
            lat = loc_json['latitude']
            lon = loc_json['longitude']


            weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s" % (weather_api_token, lat,lon)
            req = requests.get(weather_req_url, timeout=1)
            weather_json = json.loads(req.text)
            degree_symbol = u'\N{DEGREE SIGN}'
            far = int(weather_json['currently']['temperature'])
            cel = int(5 * (far - 32) / 9)

            newTemp = "%s%s" % (str(far), degree_symbol)
            newCurrently = weather_json['currently']['summary']
            newForecast = weather_json['hourly']['summary']
            iconID = weather_json['currently']['icon']
            icon2 = None
            if iconID in icon_lookup:
                icon2 = icon_lookup[iconID]

            # Display icon image from assets
            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = cv2.imread(icon2)
                    image = cv2.resize(image, (50, 50), interpolation=cv2.INTER_CUBIC)
                    image = QImage(image, image.shape[1], image.shape[0],
                    image.strides[0], QImage.Format_RGB888)

                    self.iconLabel.setPixmap(QPixmap.fromImage(image))
            else:
                self.iconLbl.setPixmap(QPixmap('')) # Remove image

            if self.currently != newCurrently:
                self.currently = newCurrently
                temp = "<font color='white'>" + newCurrently + "</font>"
                self.currentlyLabel.setText(temp)

            if self.forecast != newForecast:
                self.forecast = newForecast
                newForecast = newForecast.replace("<", "less than")
                newForecast = newForecast.replace(">", "more than")
                temp = "<font color='white'>" + newForecast + "</font>"
                self.forecastLabel.setText(temp)

            if self.temperature != newTemp:
                self.temperature = newTemp
                temp = "<font color='white'>" + newTemp + "</font>"
                self.tempLabel.setText(temp)

            newLoc = "%s, %s" % (loc_json['city'], loc_json['region_code'])
            temp = "<font color='white'>" + newLoc + "</font>"
            self.locLabel.setText(temp)

        except Exception as e:
            print("Error")













