from process import core
from gmail import api
from typing import List, Dict

COLUMNS = ['id', 'From', 'Subject', 'Read', 'Attachments', 'Received On', 'Label', 'Archived']
DB_COLUMNS = ['id', 'from_address', 'subject', 'is_read', 'has_attachment', 'received_on', 'label', 'is_archived']


def extract_email_queryset() -> List:
    all_emails = core.get_all_emails()
    email_list = []
    for email in all_emails:
        email_list.append(email.__dict__)
    return email_list


def modify_email(message_label_obj, gmail_service=api.get_gmail_service()) -> None:
    api.modify_message(service=gmail_service,
                       user_id="me",
                       msg_labels=message_label_obj)
    return None
