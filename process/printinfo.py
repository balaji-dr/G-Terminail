from typing import List
from prettytable import PrettyTable
from process.manager import RuleManager
from process import composed


COLUMNS = ['id', 'From', 'Subject', 'Read', 'Attachments', 'Received On', 'Label', 'Archived']
DB_COLUMNS = ['id', 'from_address', 'subject', 'is_read', 'has_attachment', 'received_on', 'label', 'is_archived']


def print_n_emails(emails: List) -> None:
    """Prints list of emails in table format."""
    x = PrettyTable(padding_width=0)
    x.field_names = COLUMNS
    for email in emails:
        x.add_row([email.get(column) for column in DB_COLUMNS])
    print(x)


def print_rule_predicate():
    """Prints Options for rule predicate as table."""
    x = PrettyTable()
    x.field_names = ["CHOICE", "PREDICATE"]
    x.add_row(["1", "ALL"])
    x.add_row(["2", "ANY"])
    x.add_row(["q", "QUIT"])
    print(x)


def print_date_units():
    """Prints options of date units as table."""
    x = PrettyTable()
    x.field_names = ["CHOICE", "UNIT"]
    x.add_row(["1", "Days"])
    x.add_row(["2", "Months"])
    print(x)


def print_string_fields():
    """Prints options of String fields as table."""
    x = PrettyTable()
    x.add_column("CHOICE", range(1, len(RuleManager.all_fields)+1))
    x.add_column("FIELDS", RuleManager.all_fields)
    print(x)


def print_field_predicates():
    """Prints choice of the string predicates as table."""
    x = PrettyTable()
    x.add_column("CHOICE", [1, 2, 3, 4])
    x.add_column("Predicate", ["contains", "does_not_contain", "equals", "does_not_equal"])
    print(x)


def print_date_predicates():
    """Prints choice of date predicates as table."""
    x = PrettyTable()
    x.add_column("CHOICE", [1, 2])
    x.add_column("Predicate", ["less_than", "greater_than"])
    print(x)


def print_mark_email_options():
    """Prints choice to Mark as Read/Unread as table."""
    x = PrettyTable()
    x.add_column("CHOICE", [1, 2])
    x.add_column("Label", ['READ', 'UNREAD'])
    print(x)


def print_actions():
    """Prints the choice of actions that can be performed on the emails."""
    x = PrettyTable()
    x.add_column("CHOICE", [1, 2, 3])
    x.add_column("ACTIONS", ['Mark as Read/UnRead', 'Archive', 'Add Label'])
    print(x)


def print_main_menu():
    """Prints the main menu options as a table."""
    x = PrettyTable(padding_width=1)
    x.add_column("CHOICE", [1, 2, 3, 4, 5])
    x.add_column("ACTIONS", ["RE-RUN", "VIEW SINGLE MAIL", "SYNC WITH GMAIL", "VIEW ALL EMAILS", "EXIT"])
    print(x)


def print_single_message(mail_id: int):
    """Prints the email information as a table."""
    message = composed.extract_single_message(mail_id=mail_id)
    x = PrettyTable(padding_width=0)
    x.field_names = COLUMNS + ['Message Body']
    message_details = [message.get(column) for column in DB_COLUMNS]
    message_body = message.get("message_body")
    message_details.append(message_body)
    x.add_row(message_details)
    print(x)
