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
import smartMirrorManager

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = 'MirrorX'

class Calendar(QWidget):
    def __init__(self):
        super(Calendar, self).__init__()
        self.initUI()

    def initUI(self):
        self.titleFont = QFont('Helvetica', smartMirrorManager.title_fontsize)
        self.contentFont = QFont('Helvetica', 20)

        self.calendarRows = QFormLayout()
        self.calendarRows.setVerticalSpacing(15)
        self.calendarRows.setHorizontalSpacing(40)

        self.calendarTitle = QLabel("<font color='white'>Today's Events</font>")
        self.calendarTitle.setFont(self.titleFont)
        self.calendarRows.addRow(self.calendarTitle)

        self.setLayout(self.calendarRows)

        self.getDailyEvents()
        self.updateDailyEvents()

    def updateDailyEvents(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getDailyEvents)
        self.timer.start(1000 * 60 * 60)  # Update calendar every hour

    def getDailyEvents(self):
        # Creates a Google Calendar API service object gets the daily meetings for someone (max is 10)
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC
        eventsResult = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        curr_date = time.strftime("%d")
        curr_month = time.strftime("%m")
        curr_year = time.strftime("%Y")
        num_events_today = 0

        for event in events:
            event_date = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime("%d")
            event_month = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime("%m")
            event_year = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime("%Y")
            if (curr_date == event_date and curr_month == event_month and curr_year == event_year):
                num_events_today = num_events_today + 1

        if not events or num_events_today == 0:
            relaxLabel = QLabel("<font color='white'>Time to Relax!</font>")
            noEventsLabel = QLabel("<font color='white'>No scheduled events today.</font>")
            relaxLabel.setFont(self.contentFont)
            noEventsLabel.setFont(self.contentFont)
            self.calendarRows.addRow(relaxLabel)
            self.calendarRows.addRow(noEventsLabel)

        else:
            for event in events:
                event_date = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime("%d")

                # Retrieved event may be for next day, ensure that it is today
                if (curr_date == event_date and curr_month == event_month and curr_year == event_year):
                    eventStart = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime("%I:%M %p").lstrip('0')
                    eventEnd = dateutil.parser.parse(event['end'].get('dateTime', event['end'].get('date'))).strftime("%I:%M %p").lstrip('0')
                    eventName = event['summary']

                    newEventName = QLabel("<font color='white'>" + eventName + "</font>")
                    newEventName.setWordWrap(True)
                    newEventName.setAlignment(Qt.AlignRight)
                    newEventName.setFixedWidth(150)
                    newEventTime = QLabel("<font color='white'>" + eventStart + "</font>")
                    newEventName.setFont(self.contentFont)
                    newEventTime.setFont(self.contentFont)
                    newEventTime.setAlignment(Qt.AlignRight)
                    self.calendarRows.addRow(newEventTime, newEventName)


    def get_credentials(self):
        # Gets valid user credentials from storage.
        # If nothing has been stored, or if the stored credentials are invalid, the OAuth2 flow is completed to obtain the new credentials.

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)

        return credentials