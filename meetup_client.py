import meetup.api

class MeetupClient():
    def __init__(self, api_key):
        self.client = meetup.api.Client(api_key)

    def getRsvpsForMeetup(self, eventId):
        rsvps = []
        try:
            rsvps = self.client.GetRsvps(event_id=eventId)
        except Exception as e:
            raise Exception('Failed to retrieve RSVPs for event: ' + str(e))
        return rsvps.results

    def getUpcomingEventForGroup(self, groupUrlname):
        events = []
        try:
            events = self.client.GetEvents(group_urlname=groupUrlname, status='upcoming').results
        except Exception as e:
            raise Exception(f'Failed to fetch upcoming event for group {groupUrlname}: ' + str(e))
        if not len(events):
            return None
        return events[0]
