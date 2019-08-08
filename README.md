# MeetUp Notifier

This little application (designed to run as an AWS Lambda) will send notifications based on information retrieved via the [MeetUp API](https://www.meetup.com/meetup_api/)

## Supported Notification Methods

* Email (Amazon SES)

## Requirements

* AWS account

## Environment variables

Most parameters to configure the notifier are passed in via environment variables. These variables are:

* `API_KEY`: private MeetUp API key
* `SENDER`: Amazon SES email address that will appear as the sender when email notifications are sent out.
* `RECIPIENTS`: comma-separated list of email addresses to receive the notifications. The email addresses need to be verified in AWS SES beforehand.
* `GROUP_URLNAME`: MeetUp URL name of the MeetUp group. Usually the name after the MeetUp domain on the URL, e.g. https://meetup.com/My-Group/
* `HOURS_BEFORE_NOTIFY`: minimum amount of hours before the upcoming event starts to start sending notifications. E.g. to start sending notifications 2 days prior to the event, set this value to 48.

## Running

Run locally

```
$ pip3 install -r ./requirements.txt
$ python3 app.py
```

Make sure you've got a default AWS profile defined in `~/.aws`.

Or if you want to deploy it as an AWS Lambda

```
$ make lambdify
```

And then simply upload the resulting ZIP archive to Lambda.

## TODO

See [project's kanban board](https://github.com/dvejmz/meetup-notifier/projects/1) to find out about any upcoming features and how their development is progressing.
