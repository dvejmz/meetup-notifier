import meetup.api

class MeetupClient():
    def __init__(self, api_key):
        self.client = meetup.api.Client(api_key)

    def getRsvpsForMeetup(self, eventId):
        rsvps = self.client.GetRsvps(event_id=eventId)
        return rsvps
