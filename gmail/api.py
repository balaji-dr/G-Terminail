import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from typing import List, Any
from config.settings import MAX_RESULTS_PER_PAGE, TOTAL_PAGES_TO_READ
from model import ROOT_DIR

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Returns gmail service object.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{ROOT_DIR}/gmail/client_id.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_message(msg_id: str, service, user_id='me'):
    """
    Get a Message with given ID.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

    Returns:
    A Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return 0


def get_all_mails_from_gmail() -> List:
    mails = []
    service = get_gmail_service()
    emails = service.users().messages()
    request = emails.list(userId='me', labelIds=['INBOX'], maxResults=MAX_RESULTS_PER_PAGE)
    pages = 0
    while request and pages <= TOTAL_PAGES_TO_READ-1:
        response = request.execute()
        pages += 1
        messages = response.get('messages', [])

        if not messages:
            print("No messages found.")
        else:
            mails += messages
        request = service.users().messages().list_next(previous_request=request, previous_response=response)
    return mails
