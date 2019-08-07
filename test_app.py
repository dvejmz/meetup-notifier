import unittest
from unittest.mock import Mock, MagicMock, patch
import json
import datetime
from ses_client import SesClient
from meetup_client import MeetupClient
from app import App

GROUP_URLNAME = 'Group-Urlname'
NOW = datetime.datetime.now()
DEFAULT_EVENT_START_TIME_HOURS_FROM_NOW = 48
DEFAULT_NOTIFY_PERIOD_HOURS = 72
EVENT_START_TIME = (NOW.timestamp() + (3600 * DEFAULT_EVENT_START_TIME_HOURS_FROM_NOW)) * 1000

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
        'time': EVENT_START_TIME,
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
    def test_it_exits_with_fail_return_code_if_no_notifications_sent(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=MagicMock(results=[]),
            event=getFixtureEvent(),
        )
        app = App(sesClient, meetupClient)
        self.assertFalse(app.run(GROUP_URLNAME, DEFAULT_NOTIFY_PERIOD_HOURS))

    def test_it_sends_email_when_there_are_rsvps_answers(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(),
            event=getFixtureEvent(),
        )

        app = App(sesClient, meetupClient)
        app.run(GROUP_URLNAME, DEFAULT_NOTIFY_PERIOD_HOURS)
        expectedEventStartTime = datetime.datetime.fromtimestamp(getFixtureEvent()['time'] / 1000)
        sesClient.send.assert_called_with(f'RSVPs for Group-Urlname event on {str(expectedEventStartTime)} (UTC)', f'RSVP answers for the Group-Urlname MeetUp event scheduled on {str(expectedEventStartTime)} (UTC)\n\nI have a disability\nI have another disability')

    def test_it_does_not_send_email_when_there_are_no_rsvp_answers(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(False),
            event=getFixtureEvent(),
        )

        app = App(sesClient, meetupClient)
        app.run(GROUP_URLNAME, DEFAULT_NOTIFY_PERIOD_HOURS)
        sesClient.send.assert_not_called()

    def test_it_gets_rsvps_for_upcoming_event(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(),
            event=getFixtureEvent(),
        )

        app = App(sesClient, meetupClient)
        app.run(GROUP_URLNAME, DEFAULT_NOTIFY_PERIOD_HOURS)
        meetupClient.getRsvpsForMeetup.assert_called_with(getFixtureEvent()['id'])

    def test_it_exits_if_it_cannot_find_upcoming_event(self):
        sesClient = getSesClientMock()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(),
            event=None,
        )

        app = App(sesClient, meetupClient)
        self.assertFalse(app.run(GROUP_URLNAME, DEFAULT_NOTIFY_PERIOD_HOURS))

    def test_it_exits_if_upcoming_event_is_far_into_the_future(self):
        sesClient = getSesClientMock()
        eventFixture = getFixtureEvent()
        meetupClient = getMeetupClientMock(
            rsvps=getFixtureRsvps(),
            event=eventFixture,
        )

        app = App(sesClient, meetupClient)
        sesClient.send.assert_not_called()
        self.assertFalse(app.run(GROUP_URLNAME, 1))
