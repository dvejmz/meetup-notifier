import unittest
import datetime

import email_compose

class Test(unittest.TestCase):
    def test_it_returns_valid_email(self):
        fixtures = [
            {'answers': ['I have a requirement']},
            {'answers': []},
            {'answers': ['I have another requirement']},
        ]
        expected = 'RSVP answers for the Group-Urlname MeetUp event scheduled on 2019-08-06 23:32:47\n\nI have a requirement\nI have another requirement'
        result = email_compose.composeEmail('Group-Urlname', datetime.datetime.fromtimestamp(1565130767000/1000), ['I have a requirement', 'I have another requirement'])
        self.assertEqual(expected, result)
