import boto3

class SesClient():
    def __init__(self, fromAddress, toAddresses):
        self.ses = boto3.client('ses')
        self.fromAddress = fromAddress
        self.toAddresses = toAddresses

    def send(self, message):
        response = self.ses.send_email(
            Source=self.fromAddress,
            Destination={
                'ToAddresses': self.toAddresses,
            },
            Message={
                'Subject': {
                    'Data': 'RSVP Summary',
                },
                'Body': {
                    'Text': {
                        'Data': message,
                    }
                },
            }
        )
        print(response)
