
from __future__ import print_function

import dateutil.parser
import httplib2
import os
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

from smartMirrorManager import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Constants
small_fontsize = 12
med_fontsize = 22
large_fontsize = 32
xlarge_fontsize = 41

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

class Calendar(QWidget):
    def __init__(self):
        super(Calendar, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', med_fontsize)

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
        self.getNextMeeting()

    def getNextMeeting(self):
        # Creates a Google Calendar API service object and outputs a list of the next 10 events on the user's calendar.

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            self.lbl1.setText("<font color='white'>" + "Time to relax!" + "</font>")
            self.lbl2.setText("<font color='white'>" + "Looks like you have no upcoming events today." + "</font>")
        else:
            curr_date = time.strftime("%d")
            num_events_today = 0

            for event in events:
                event_date = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime("%d")
                if (curr_date == event_date):
                    num_events_today = num_events_today + 1

            if num_events_today == 0:
                self.lbl1.setText("<font color='white'>" + "Time to relax!" + "</font>")
                self.lbl2.setText("<font color='white'>" + "Looks like you have no upcoming events today." + "</font>")
            else:
                event = events[0]
                event_date = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime("%d")

                if(curr_date == event_date):
                    start = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime("%I:%M %p")
                    end = dateutil.parser.parse(event['end'].get('dateTime', event['end'].get('date'))).strftime("%I:%M %p")
                    title = event['summary']
                    text1 = ""
                    text2 = ""

                    if(num_events_today > 1):
                        text1 = "You have " + str(num_events_today) + " meetings" + " today."
                        text2 = "The first one is: " + events[0]['summary'] + ", which starts at " + start + " and ends at " + end
                    else:
                        text1 = "You only have one meeting today: " + event['summary']
                        text2 = "It starts at " + start + " and ends at " + end

                    self.lbl1.setText("<font color='white'>" + text1  + "</font>")
                    self.lbl2.setText("<font color='white'>" + text2 + ".</font>")


    def get_credentials(self):
        # Gets valid user credentials from storage.
        # If nothing has been stored, or if the stored credentials are invalid, the OAuth2 flow is completed to obtain the new credentials.

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
