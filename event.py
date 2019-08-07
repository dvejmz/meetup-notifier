import datetime

def eventStartTimestampToDateTime(event):
    eventStartEpochSeconds = event['time'] / 1000
    return datetime.datetime.fromtimestamp(eventStartEpochSeconds)

def getEventStartTimeFromDateInSeconds(event, sourceDate):
    eventStartEpochSeconds = event['time'] / 1000
    sourceDateEpochSeconds = sourceDate.timestamp()
    return eventStartEpochSeconds - sourceDateEpochSeconds

