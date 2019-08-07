def composeEmail(groupName, eventStartDateTime, answers):
    messageAnswers = '\n'.join(answers)
    return f'RSVP answers for the {groupName} MeetUp event scheduled on {str(eventStartDateTime)} (UTC)\n\n{messageAnswers}'
