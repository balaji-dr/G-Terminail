from typing import List
from prettytable import PrettyTable
from process.manager import RuleManager

COLUMNS = ['id', 'From', 'Subject', 'Read', 'Attachments', 'Received On', 'Label', 'Archived']
DB_COLUMNS = ['id', 'from_address', 'subject', 'is_read', 'has_attachment', 'received_on', 'label', 'is_archived']


def print_n_emails(emails: List) -> None:
    x = PrettyTable(padding_width=1)
    x.field_names = COLUMNS
    for email in emails:
        x.add_row([email.get(column) for column in DB_COLUMNS])
    print(x)


def print_rule_predicate():
    x = PrettyTable()
    x.field_names = ["CHOICE", "PREDICATE"]
    x.add_row(["1", "ALL"])
    x.add_row(["2", "ANY"])
    x.add_row(["q", "QUIT"])
    print(x)


def print_date_units():
    x = PrettyTable()
    x.field_names = ["CHOICE", "UNIT"]
    x.add_row(["1", "Days"])
    x.add_row(["2", "Months"])
    print(x)


def print_string_fields():
    x = PrettyTable()
    x.add_column("CHOICE", range(1, len(RuleManager.string_fields + RuleManager.date_field)+1))
    x.add_column("FIELDS", RuleManager.string_fields + RuleManager.date_field)
    print(x)


def print_field_predicates():
    x = PrettyTable()
    x.add_column("CHOICE", [1, 2, 3, 4])
    x.add_column("Predicate", ["contains", "does_not_contain", "equals", "does_not_equal"])
    print(x)


def print_date_predicates():
    x = PrettyTable()
    x.add_column("CHOICE", [1, 2])
    x.add_column("Predicate", ["less_than", "greater_than"])
    print(x)


def print_mark_email_options():
    x = PrettyTable()
    x.add_column("CHOICE", [1, 2])
    x.add_column("Label", ['READ', 'UNREAD'])
    print(x)


def print_actions():
    x = PrettyTable()
    x.add_column("CHOICE", [1, 2, 3])
    x.add_column("ACTIONS", ['Mark as Read/UnRead', 'Archive', 'Add Label'])
    print(x)

