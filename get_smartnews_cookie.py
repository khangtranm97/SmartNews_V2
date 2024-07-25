#Login
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json
import msvcrt
import os.path
import base64
import email
import json 
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build



#Path folder define
if getattr(sys, 'frozen', False):  # Check if running as compiled executable
        script_path = sys.executable  # Path of the executable
else:
        script_path = os.path.abspath(__file__) 
file_contain_folder = os.path.dirname(script_path)


#Get config file for running info
config_path=file_contain_folder+'\\config.json'
with open(config_path, 'r') as file:
    data = json.load(file)

#Set browser options
driver = webdriver.Chrome()
login_code_input_xpath='//*[@id="app"]/div/section/div/div/div/div/div[2]/div[1]/div/form/div[1]/div/input'
login_xpath='//*[@id="app"]/div/section/div/div/div/div/div[2]/div[1]/div/form/div[2]/button'
mailaddress =data['mailaddress']
work_url=data['work_url']
page_address="//html/body/div/form/div/div[1]/div[2]/div/div[3]/button"



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


def get_cookie():
    print('------------------------------------------------------------------------')
    print('RUN')
    driver.get(work_url)
    time.sleep(2)
    controller = driver.find_element(By.XPATH, page_address)
    controller.click()

    #Login email input
    input=driver.find_element(By.CLASS_NAME,'input')
    time.sleep(1)
    input.send_keys(mailaddress)

    #Send code
    codesender=driver.find_element(By.CLASS_NAME,'button.is-dark.is-fullwidth')
    time.sleep(1)
    codesender.click()
    print('Login by code selected. Code sended to your email address !')
    print('Wait for login code')
    time.sleep(30)
    #Get login token
    login_token=get_token()
    controller=driver.find_element(By.XPATH,login_code_input_xpath)
    controller.send_keys(login_token) 
    controller=driver.find_element(By.XPATH,login_xpath)
    controller.click()
    print('Login Completed')

    time.sleep(5)
    print('Saving Cookie')
    cookies = driver.get_cookies()
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)
    print('Cookie saved')
    driver.quit()
    print("Press any key to continue...")
    msvcrt.getch()
get_cookie()