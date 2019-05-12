import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from typing import List
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
        print(f'An error occurred: {error}')


def get_all_mails_from_gmail() -> List:
    """
    Get all the message objects from the user's account.

    Returns:
    A List of message objects.
    """
    try:
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
            request = service.users().messages().list_next(previous_request=request,
                                                           previous_response=response)
        return mails
    except errors.HttpError as error:
        print(f'An error occurred: {error}')


def modify_message(msg_labels, service=get_gmail_service(), user_id='me'):
    """Modify the Labels on the given Message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The id of the message required.
    msg_labels: The change in labels.

    Returns:
    Modified message, containing updated labelIds, id and threadId.
    """

    try:
        message = service.users().messages().batchModify(userId=user_id, body=msg_labels).execute()
        return message
    except errors.HttpError as e:
        print(f'An error occurred: {e}')


def create_label(service, user_id, label_object):
    """Creates a new label within user's mailbox, also prints Label ID.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_object: label to be added.
    Returns:
        Created Label.
    """
    try:
        label = service.users().labels().create(userId=user_id,
                                                body=label_object).execute()
        return label
    except errors.HttpError as e:
        print(f'An error occurred: {e}')


def make_label(label_name, mlv='show', llv='labelShow'):
    """Create Label object.

    Args:
    label_name: The name of the Label.
    mlv: Message list visibility, show/hide.
    llv: Label list visibility, labelShow/labelHide.

    Returns:
    Created Label.
    """
    label = {
        'messageListVisibility': mlv,
        'name': label_name,
        'labelListVisibility': llv
    }
    return label


def list_labels(service, user_id):
    """Get a list all labels in the user's mailbox.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.

    Returns:
    A list all Labels in the user's mailbox.
    """
    try:
        response = service.users().labels().list(userId=user_id).execute()
        labels = response['labels']
        return labels
    except errors.HttpError as e:
        print(f'An error occurred: {e}')


def list_user_labels() -> List:
    """
    Get a list of all user created labels.
    :return: List of label data.
    """
    try:
        all_labels = list_labels(service=get_gmail_service(), user_id="me")
        user_labels = [label for label in all_labels]
        for label in user_labels[:]:
            if label.get("type") != 'user':
                user_labels.remove(label)
        return user_labels
    except errors.HttpError as e:
        print(f"Error occured: {e}")

# print(list_user_labels())
