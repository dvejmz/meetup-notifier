import meetup.api

class MeetupClient():
    def __init__(self, api_key):
        self.client = meetup.api.Client(api_key)

    def getRsvpsForMeetup(self, eventId):
        rsvps = self.client.GetRsvps(event_id=eventId)
        return rsvps.results

    def getUpcomingEventForGroup(self, groupUrlname):
        events = self.client.GetEvents(group_urlname=groupUrlname, status='upcoming')
        return events.results[0]
