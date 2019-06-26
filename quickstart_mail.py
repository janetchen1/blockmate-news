from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def main():
    mail_creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('mail_token.pickle'):
        with open('mail_token.pickle', 'rb') as mail_token:
            mail_creds = pickle.load(mail_token)
    # If there are no (valid) credentials available, let the user log in.
    if not mail_creds or not mail_creds.valid:
        if mail_creds and mail_creds.expired and mail_creds.refresh_token:
            mail_creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            mail_creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('mail_token.pickle', 'wb') as mail_token:
            pickle.dump(mail_creds, mail_token)

if __name__ == '__main__':
    main()