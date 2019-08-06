def getAnswersfromRsvps(rsvps):
    answers = []
    for r in rsvps:
        rsvp_answers = list(filter(lambda a: len(a), r['answers']))
        if len(rsvp_answers):
            answers.extend(r['answers'])
    return answers

