import unittest
from unittest.mock import Mock, MagicMock, patch
import json
from ses_client import SesClient
from meetup_client import MeetupClient
from app import App

def getMeetupClientMock(rsvps={}):
    mock = MagicMock(wraps=MeetupClient)
    mock.getRsvpsForMeetup.return_value = rsvps
    return mock

def getSesClientMock():
    mock = MagicMock(wraps=SesClient)
    mock.send.return_value = True
    return mock

class Test(unittest.TestCase):
    def test_it_exits_successfully(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=MagicMock(results=[])
        )
        app = App(sesClient, meetupClient)
        self.assertTrue(app.run())

    def test_it_sends_email_when_there_are_rsvps_answers(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=MagicMock(results=
                [
                    {'answers': ['I have a disability']},
                    {'answers': []},
                    {'answers': ['I have another disability']},
                ]
            ))

        app = App(sesClient, meetupClient)
        appOutput = app.run()
        sesClient.send.assert_called_with('I have a disability\nI have another disability')
        self.assertTrue(appOutput)

    def test_it_does_not_send_email_when_there_are_no_rsvp_answers(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=MagicMock(results=
                [
                    {'answers': []},
                    {'answers': []},
                    {'answers': []},
                ]
            ))

        app = App(sesClient, meetupClient)
        appOutput = app.run()
        sesClient.send.assert_not_called()
        self.assertTrue(appOutput)
