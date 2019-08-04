import logging
import os
import sys
from datetime import datetime

from meetup_client import MeetupClient
from ses_client import SesClient

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class App():
    def __init__(self, sesClient, meetupClient):
        self.sesClient = sesClient
        self.meetupClient = meetupClient

    def getAnswersfromRsvps(self, rsvps):
        answers = []
        for r in rsvps:
            rsvp_answers = list(filter(lambda a: len(a), r['answers']))
            if len(rsvp_answers):
                answers.extend(r['answers'])
        return answers

    def composeEmail(self, groupName, eventStartDateTime, answers):
        messageAnswers = '\n'.join(answers)
        return f'RSVP answers for the {groupName} MeetUp event scheduled on {str(eventStartDateTime)}\n\n{messageAnswers}'

    def run(self, groupUrlname):
        upcomingEvent = self.meetupClient.getUpcomingEventForGroup(groupUrlname)
        if upcomingEvent is None:
            logger.info('No upcoming event found, exiting')
            return False

        eventStartEpochSeconds = upcomingEvent['time'] / 1000
        eventStartDateTime = datetime.fromtimestamp(eventStartEpochSeconds)
        logger.info('Upcoming event found. Starting on ' + str(eventStartDateTime))
        rsvps = self.meetupClient.getRsvpsForMeetup(upcomingEvent['id'])
        rsvpsWithAnswers = self.getAnswersfromRsvps(rsvps)
        numRsvps = len(rsvps)
        numRsvpsWithAnswers = len(rsvpsWithAnswers)
        if (numRsvpsWithAnswers):
            logger.info(f'Total RSVPs: {numRsvps}. RSVPs w/ Answers: {numRsvpsWithAnswers}. Sending notification')
            body = self.composeEmail(groupUrlname, eventStartDateTime, rsvpsWithAnswers)
            self.sesClient.send(f'RSVPs for {groupUrlname} event on {str(eventStartDateTime)}', body)
        else:
            logger.info('No RSVPs found, exiting')
            return False
        
        logger.info('Done')
        return True

def start():
    apiKey = os.environ.get('API_KEY')
    if not apiKey:
        raise Exception('API key not provided')
    meetupClient = MeetupClient(apiKey)
    fromAddress = os.environ.get('SENDER')
    if not len(fromAddress):
        raise Exception('No sender email provided')
    toAddressesCsv = os.environ.get('RECIPIENTS')
    if not len(toAddressesCsv):
        raise Exception('No CSV list of recipients was provided')
    toAddresses = toAddressesCsv.split(',')
    sesClient = SesClient(fromAddress, toAddresses)
    groupUrlname = os.environ.get('GROUP_URLNAME')
    if not len(groupUrlname):
        raise Exception('No group urlname provided')
    app = App(sesClient, meetupClient)
    return app.run(groupUrlname)

if __name__ == "__main__":
    start()
