from process import core
from typing import List, Dict

COLUMNS = ['id', 'From', 'Subject', 'Read', 'Attachments', 'Received On', 'Label', 'Archived']
DB_COLUMNS = ['id', 'from_address', 'subject', 'is_read', 'has_attachment', 'received_on', 'label', 'is_archived']


def extract_email_queryset() -> List[Dict]:
    """
    Extracts all the email attributes from the database object.
    :return: List of dicts containing email attributes.
    :rtype: list
    """
    all_emails = core.get_all_emails()
    email_list = []
    for email in all_emails:
        email_list.append(email.__dict__)
    return email_list


def extract_single_message(mail_id: int) -> Dict:
    """
    Extracts single email attributes from the database object.
    :param mail_id: Id of the specific message in the database.
    :return: Attributes of the email.
    :rtype: dict
    """
    message = core.get_single_message_object(mail_id=mail_id)
    return message.__dict__
