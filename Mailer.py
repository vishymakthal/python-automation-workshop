from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
import datetime

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

USER_EMAIL = 'vmaktha@ncsu.edu'
BOT_EMAIL = 'vishy.makthal@gmail.com'

SCOPES = 'https://mail.google.com/'

def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """

  msgRoot = MIMEMultipart('related')
  msgRoot['subject'] = subject
  msgRoot['from'] = sender
  msgRoot['to'] = to

  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

  msgText = MIMEText(message_text, 'html')
  msgAlternative.attach(msgText)
  return {'raw': base64.urlsafe_b64encode(msgRoot.as_string().encode('ASCII')).decode()}


def get_credentials():
    store = file.Storage('mail_token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service


def send_reminder_email(items):

    service = get_credentials()

    message ='''

            <html><h3> Review Reminder for (''' + str(datetime.date.today()) + ''') </h3>

            <h4> Up For Review Today </h4>
            <hr/>
            <ul>
            '''

    for it in items:
        message += '<li>{}</li>'.format(it)

    message += "<hr/></ul></html>"

    msg = CreateMessage(BOT_EMAIL, USER_EMAIL, '[TEST] Review Reminder', message)
    SendMessage(service, BOT_EMAIL, msg)

if __name__ == "__main__":
    send_reminder_email([])
