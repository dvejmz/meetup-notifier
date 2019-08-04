import logging
import os

from meetup_client import MeetupClient
from ses_client import SesClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

        response = self.meetupClient.getRsvpsForMeetup(upcomingEvent['id'])
        rsvps = response.results
        rsvps_with_answers = self.getAnswersfromRsvps(rsvps)
        if (len(rsvps_with_answers)):
            logger.info('RSVPs were found, sending notification')
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
