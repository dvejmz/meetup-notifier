import boto3

class SesClient():
    def __init__(self, fromAddress, toAddresses):
        self.ses = boto3.client('ses')
        self.fromAddress = fromAddress
        self.toAddresses = toAddresses

    def send(self, subject, body):
        try:
            response = self.ses.send_email(
                Source=self.fromAddress,
                Destination={
                    'ToAddresses': self.toAddresses,
                },
                Message={
                    'Subject': {
                        'Data': subject,
                    },
                    'Body': {
                        'Text': {
                            'Data': body,
                        }
                    },
                }
            )
        except Exception as e:
            raise Exception('Failed to send SES email: ' + str(e))
