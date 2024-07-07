import os.path
import base64
import email
import json 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_message(service, user_id, msg_id):
    """Get a Message with given ID."""
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        payload = message['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")
        
        email_data = {}
        
        for header in headers:
            if header['name'] == 'From':
                email_data['from'] = header['value']
            if header['name'] == 'To':
                email_data['to'] = header['value']
            if header['name'] == 'Subject':
                email_data['subject'] = header['value']
            if header['name'] == 'Date':
                email_data['date'] = header['value']
                
        # The email body might be split into several parts
        if parts:
            for part in parts:
                mime_type = part['mimeType']
                body = part['body']
                data = body.get('data')
                if data:
                    text = base64.urlsafe_b64decode(data).decode('utf-8')
                    email_data['body'] = text
        else:
            # Fallback for when parts are not available
            data = payload.get('body').get('data')
            if data:
                text = base64.urlsafe_b64decode(data).decode('utf-8')
                email_data['body'] = text
        
        return email_data

    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def get_token():
    login_token=""
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail messages.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', maxResults=1, q='subject:"SmartNews Sign-in Passcode"+is:unread').execute()
    messages = results.get('messages', [])

    mail_data = []
    if not messages:
        print('No messages found.')
    else:
        print('New Mail Arrived. Checking for login token')
        for message in messages:
            email_data = get_message(service, 'me', message['id'])
            #if email_data:
            #    print(f"From: {email_data.get('from')}")
            #    print(f"To: {email_data.get('to')}")
            #    print(f"Subject: {email_data.get('subject')}")
            #    print(f"Date: {email_data.get('date')}")
            #    print(f"Body: {email_data.get('body')}")
            #    print() 
        raw_token=""
        raw_token=email_data.get('body')
        start_place=raw_token.find('following code:')
        login_token=raw_token[start_place+31:start_place+37]
        print('Get log in token successful')
    return login_token

if __name__ == '__get_token__':
    get_token()
