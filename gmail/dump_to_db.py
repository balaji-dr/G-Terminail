from gmail import api
from model import Email, engine
import base64
import re
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from apiclient import errors
from typing import List, Dict
from dateutil.parser import parse
from progress.bar import Bar
from config.settings import MAX_RESULTS_PER_PAGE, TOTAL_PAGES_TO_READ


DBSession = sessionmaker(bind=engine)
session = DBSession()

MIME_TYPES = ['multipart/alternative', 'multipart/mixed', 'multipart/related', 'text/plain', 'text/html']


def parse_message_headers(headers: List) -> Dict:
    """
    Parse the headers of the email to extract only the required.
    :param headers: The list of headers of an email message.
    :type headers: list
    :return: Dictionary of the header name and its value.
    :rtype: dict
    """
    header_dict = {}
    for header in headers:
        if header['name'] == 'Delivered-To':
            header_dict['to_address'] = header['value']
        if header['name'] == 'Subject':
            header_dict["subject"] = header['value']
        if header['name'] == 'From':
            header_dict["from_address"] = header['value']
        if header['name'] == 'Date':
            header_dict['received_on'] = parse(header['value'])
    return header_dict


def parse_message_payload(payload: Dict, message='', attachment=False) -> (str, bool):
    """
    Parses the Gmail API message body recursively by processing
    based on the mime type of the object.

    :param payload: Message object from Gmail API.
    :type payload: dict

    :param message: Email content.
    :type message: str

    :param attachment: Presence of an email attachment.
    :type attachment: bool

    :return: A tuple of the message and the presence of attachment.
    :rtype: tuple
    """
    if payload['mimeType'] == 'multipart/mixed' or payload['mimeType'] == 'multipart/alternative' \
            or payload['mimeType'] == 'multipart/related':
        parts_data = payload['parts']
        for each in parts_data:
            temp, attachment = parse_message_payload(payload=each, message=message)
            if isinstance(temp, str):
                message += temp

    elif payload['mimeType'] == 'text/plain' or payload['mimeType'] == 'text/html':
        part_body = payload['body']
        part_data = part_body['data']
        clean_one = part_data.replace("-", "+")
        clean_one = clean_one.replace("_", "/")
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
        soup = BeautifulSoup(clean_two, 'lxml')
        for s in soup(['script', 'style']):
            s.decompose()
        return ' '.join(soup.stripped_strings), attachment

    elif payload['mimeType'] not in MIME_TYPES:
        attachment = True

    return message, attachment


def email_list_to_database() -> None:
    """
    Get all the email objects from the Gmail API and parses it
    to get the required fields and store it in the local database.
    :return: None
    """
    try:
        session.query(Email).delete()
        session.commit()
        bar = Bar('Processing', max=TOTAL_PAGES_TO_READ * MAX_RESULTS_PER_PAGE)
        service = api.get_gmail_service()
        all_emails = api.get_all_mails_from_gmail()
        for email in all_emails:
            message = api.get_message(user_id="me", msg_id=email['id'], service=service)
            payload = message['payload']
            temp_dict = parse_message_headers(headers=payload['headers'])
            message_body, attachment = parse_message_payload(payload=payload)
            temp_dict['message_body'] = re.sub(r'[\t\r\n]', '', message_body)
            temp_dict['has_attachment'] = attachment
            temp_dict['message_id'] = message['id']
            temp_dict['label'] = ','.join(message['labelIds'])
            if 'INBOX' not in message['labelIds']:
                temp_dict['is_archived'] = True
            else:
                temp_dict['is_archived'] = False
            if 'UNREAD' in message['labelIds']:
                temp_dict['is_read'] = False
            else:
                temp_dict['is_read'] = True
            email_obj = Email(**temp_dict)
            session.add(email_obj)
            session.commit()
            bar.next()
        bar.finish()
        print("Successfully dumped email to database!")
    except (SQLAlchemyError, errors.HttpError) as e:
        print(f"Database Syncing failed. Error is : {e}")
