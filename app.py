import logging
import os
import sys

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

    def run(self, groupUrlname):
        logger.info('Running')

        upcomingEvent = self.meetupClient.getUpcomingEventForGroup(groupUrlname)
        if upcomingEvent is None:
            logger.info('No upcoming event found, exiting')
            return False

        rsvps = self.meetupClient.getRsvpsForMeetup(upcomingEvent['id'])
        rsvps_with_answers = self.getAnswersfromRsvps(rsvps)
        num_rsvps = len(rsvps)
        num_rsvps_with_answers = len(rsvps_with_answers)
        if (num_rsvps_with_answers):
            logger.info(f'Total RSVPs: {num_rsvps}. RSVPs w/ Answers: {num_rsvps_with_answers}. Sending notification')
            message = '\n'.join(rsvps_with_answers)
            print(message)
            self.sesClient.send(message)
        else:
            logger.info('No RSVPs found')
        
        logger.info('Done')
        return True

if __name__ == "__main__":
    apiKey = os.environ.get('API_KEY')
    if not apiKey:
        raise Exception('API key not provided')
    meetupClient = MeetupClient(apiKey)
    sesClient = SesClient()
    groupUrlname = os.environ.get('GROUP_URLNAME')
    if len(groupUrlname) == 0:
        raise Exception('No group urlname provided')
    app = App(sesClient, meetupClient)
    app.run(groupUrlname)
