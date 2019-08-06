import unittest

import rsvps

class Test(unittest.TestCase):
    def test_it_extracts_answers_from_rsvps(self):
        fixtures = [
            {'answers': ['I have a requirement']},
            {'answers': []},
            {'answers': ['I have another requirement']},
        ]
        expected = ['I have a requirement', 'I have another requirement']
        result = rsvps.getAnswersfromRsvps(fixtures)

    def test_it_returns_empty_list_if_no_answers(self):
        fixtures = [
            {'answers': []},
            {'answers': []},
            {'answers': []},
        ]
        expected = []
        result = rsvps.getAnswersfromRsvps(fixtures)

