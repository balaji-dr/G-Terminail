from process import core
from typing import List, Dict
from prettytable import PrettyTable

COLUMNS = ['id', 'From', 'Subject', 'Read/Unread', 'Attachments', 'Received On', 'Label', 'Archived']
DB_COLUMNS = ['id', 'from_address', 'subject', 'is_read', 'has_attachment', 'received_on', 'label', 'is_archived']


def extract_email_queryset() -> List:
    all_emails = core.get_all_emails()
    email_list = []
    for email in all_emails:
        email_list.append(email.__dict__)
    return email_list


def print_n_emails(n: int) -> None:
    x = PrettyTable(border=False, padding_width=1)
    emails = extract_email_queryset()[:n]
    x.field_names = COLUMNS
    for email in emails:
        x.add_row([email.get(column) for column in DB_COLUMNS])
    print(x)
