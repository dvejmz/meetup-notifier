import unittest
from unittest.mock import Mock, MagicMock, patch
import json
from ses_client import SesClient
from meetup_client import MeetupClient
from app import App

GROUP_URLNAME = 'Group-Urlname'

def getMeetupClientMock(rsvps={}, event={}):
    mock = MagicMock(wraps=MeetupClient)
    mock.getRsvpsForMeetup.return_value = rsvps
    mock.getUpcomingEventForGroup.return_value = event
    return mock

def getSesClientMock():
    mock = MagicMock(wraps=SesClient)
    mock.send.return_value = True
    return mock

def getFixtureEvent():
    return {
        'id': 'i43widfjdsf',
        'description': 'This is a test event',
    }

def getFixtureRsvps(with_answers=True):
    if with_answers:
        return [
            {'answers': ['I have a disability']},
            {'answers': []},
            {'answers': ['I have another disability']},
        ]
    else:
        return [
            {'answers': []},
            {'answers': []},
            {'answers': []},
        ]

class Test(unittest.TestCase):
    def test_it_exits_successfully(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=MagicMock(results=[]),
            event=getFixtureEvent(),
        )
        app = App(sesClient, meetupClient)
        self.assertTrue(app.run(GROUP_URLNAME))

    def test_it_sends_email_when_there_are_rsvps_answers(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(),
            event=getFixtureEvent(),
        )

        app = App(sesClient, meetupClient)
        app.run(GROUP_URLNAME)
        sesClient.send.assert_called_with('I have a disability\nI have another disability')

    def test_it_does_not_send_email_when_there_are_no_rsvp_answers(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(False),
            event=getFixtureEvent(),
        )

        app = App(sesClient, meetupClient)
        app.run(GROUP_URLNAME)
        sesClient.send.assert_not_called()

    def test_it_gets_rsvps_for_upcoming_event(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(),
            event=getFixtureEvent(),
        )

        app = App(sesClient, meetupClient)
        app.run(GROUP_URLNAME)
        meetupClient.getRsvpsForMeetup.assert_called_with(getFixtureEvent()['id'])

    def test_it_exits_if_it_cannot_find_upcoming_event(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(),
            event=None,
        )

        app = App(sesClient, meetupClient)
        self.assertFalse(app.run(GROUP_URLNAME))
