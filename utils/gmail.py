import base64

from email.mime.text import MIMEText
from googleapiclient import http

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
  sender: Email address of the sender.
  to: Email address of the receiver.
  subject: The subject of the email message.
  message_text: The text of the email message.

  Returns:
  An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
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
    print 'Message Id: %s' % message['id']
    return message
  except http.HttpError:
    print 'An error occurred'

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}
