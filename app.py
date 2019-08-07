import logging
import os
import sys
from datetime import datetime

from meetup_client import MeetupClient
from ses_client import SesClient
import rsvps as Rsvps
import event as Event
import email_compose as EmailCompose

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

class App():
    def __init__(self, sesClient, meetupClient):
        self.sesClient = sesClient
        self.meetupClient = meetupClient

    def run(self, groupUrlname, hoursBeforeEventToNotify):
        upcomingEvent = self.meetupClient.getUpcomingEventForGroup(groupUrlname)
        if upcomingEvent is None:
            logger.info('No upcoming event found, exiting')
            return False

        eventStartSecondsFromNow = Event.getEventStartTimeFromDateInSeconds(upcomingEvent, datetime.now())
        secondsBeforeEventToNotify = hoursBeforeEventToNotify * 3600
        eventStartDateTime = Event.eventStartTimestampToDateTime(upcomingEvent)
        logger.info('Event starting on ' + str(eventStartDateTime))
        if eventStartSecondsFromNow > secondsBeforeEventToNotify:
            eventStartHoursFromNow = eventStartSecondsFromNow / 3600
            logger.info(f'Upcoming event too far into the future ({eventStartHoursFromNow}), exiting')
            return False

        rsvps = self.meetupClient.getRsvpsForMeetup(upcomingEvent['id'])
        rsvpsWithAnswers = Rsvps.getAnswersfromRsvps(rsvps)
        numRsvps = len(rsvps)
        numRsvpsWithAnswers = len(rsvpsWithAnswers)
        if numRsvpsWithAnswers:
            logger.info(f'Total RSVPs: {numRsvps}. RSVPs w/ Answers: {numRsvpsWithAnswers}. Sending notification')
            body = EmailCompose.composeEmail(groupUrlname, eventStartDateTime, rsvpsWithAnswers)
            self.sesClient.send(f'RSVPs for {groupUrlname} event on {str(eventStartDateTime)} (UTC)', body)
        else:
            logger.info('No RSVPs found, exiting')
            return False
        
        logger.info('Done')
        return True

def getConfig():
    apiKey = os.environ.get('API_KEY')
    if not apiKey:
        raise Exception('API key not provided')
    fromAddress = os.environ.get('SENDER')
    if not len(fromAddress):
        raise Exception('No sender email provided')
    toAddressesCsv = os.environ.get('RECIPIENTS')
    if not len(toAddressesCsv):
        raise Exception('No CSV list of recipients was provided')
    toAddresses = toAddressesCsv.split(',')
    groupUrlname = os.environ.get('GROUP_URLNAME')
    if not len(groupUrlname):
        raise Exception('No group urlname provided')
    hoursBeforeNotify = os.environ.get('HOURS_BEFORE_NOTIFY') or 48

    return {
        'apiKey': apiKey,
        'sender': fromAddress,
        'recipients': toAddresses,
        'groupUrlname': groupUrlname,
        'hoursBeforeNotify': int(hoursBeforeNotify),
    }

def start(config):
    meetupClient = MeetupClient(config['apiKey'])
    sesClient = SesClient(config['sender'], config['recipients'])
    app = App(sesClient, meetupClient)
    return app.run(config['groupUrlname'], config['hoursBeforeNotify'])

if __name__ == "__main__":
    start(getConfig())
