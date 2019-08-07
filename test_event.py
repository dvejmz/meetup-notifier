import unittest

import datetime
import event

class Test(unittest.TestCase):
    def test_it_returns_event_start_delta_from_now(self):
        eventStartTime = 1565130767000
        fixture = {
            'id': 'i43widfjdsf',
            'description': 'This is a test event',
            'time': eventStartTime,
        }
        expected = 3600
        now = datetime.datetime.fromtimestamp((eventStartTime / 1000) - expected)
        result = event.getEventStartTimeFromDateInSeconds(fixture, now)
        self.assertEqual(result, 3600)
