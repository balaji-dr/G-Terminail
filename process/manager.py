from typing import Dict, List
import operator
from process import composed, core
from datetime import datetime
from dateutil import relativedelta
from gmail import api
from config.settings import RULES


class RuleManager:
    """
    Contains variables and methods used for applying the
    rule filters on the stored emails.
    """
    all_fields = RULES["fields"]
    string_fields = ["from_address", "to_address", "subject", "message_body"]
    date_field = ["received_on"]
    date_unit_list = RULES["date_predicate"]["unit"]
    rule_dict = {}

    def __init__(self):
        """
        Initiates the class instance with variables.
        """
        self.rule_predicate = "all"
        self.date_unit = "days"
        self.query_dict = {}
        self.predicate_dict = {}
        self.all_emails = composed.extract_email_queryset()
        self.filtered_emails = []

    @staticmethod
    def predicate_converter(predicate):
        """
        Returns the function mapped to the predicate.
        :param predicate: Predicate chosen to apply.
        :return: Reference to the mapped operator function.
        """
        return {
            "contains": operator.contains,
            "does_not_contain": operator.not_,
            "equals": operator.eq,
            "does_not_equal": operator.ne,
            "less_than": operator.lt,
            "greater_than": operator.gt
        }[predicate]

    def set_rule_predicate(self, index):
        """Add a new key, value to the rule predicate dictionary."""
        self.rule_predicate = self.rule_dict["rule_predicate"][index]

    def set_date_unit(self, index):
        """Set the date unit - Days/Months."""
        self.date_unit = self.date_unit_list[index]

    def process_operation(self, operand1, operation, operand2):
        """
        Call the function based on the operation by passing the operands.
        :param operand1: First operand to be passed to the referenced function.
        :param operation: Name of the Function to be called.
        :param operand2: Second operand to be passed to the referenced function.
        :return: Returns True or False based on the operation.
        """
        if operation == "does_not_contain":
            return not self.predicate_converter("contains")(operand1, operand2)
        return self.predicate_converter(operation)(operand1, operand2)

    def set_predicate_dict(self, key: str, value: str):
        """Add a new key, value to the string predicate dictionary."""
        self.predicate_dict[key] = value

    def set_query_dict(self, key: str, value: [str, int]):
        """Add a new key, value to the query dictionary."""
        self.query_dict[key] = value

    def apply_filters(self):
        """Apply the filters based on the selected rules on the emails stored."""
        current_datetime = datetime.now()
        if len(self.predicate_dict.keys()) == 1:
            self.rule_predicate = "all"
        for email in self.all_emails:
            flag_all = False
            time_delta = current_datetime - email["received_on"]
            for field, predicate in self.predicate_dict.items():
                if field in self.date_field and self.date_unit == "days":
                    operand1 = time_delta.days
                elif field in self.date_field and self.date_unit == "months":
                    operand1 = relativedelta.relativedelta(current_datetime, email["received_on"]).months
                else:
                    operand1 = email.get(field)
                if self.process_operation(operand1=operand1,
                                          operation=predicate,
                                          operand2=self.query_dict.get(field)):
                    if self.rule_predicate == "any":
                        self.filtered_emails.append(email)
                        break
                    elif self.rule_predicate == "all":
                        flag_all = True
                else:
                    if self.rule_predicate == "all":
                        flag_all = False
                        break
                    elif self.rule_predicate == "any":
                        continue
            if flag_all:
                    self.filtered_emails.append(email)


class ProcessManager:
    """
    Contains variables and methods to perform actions
    on the filtered emails.
    """

    actions = list(RULES["actions"].keys())
    mark_as_list = RULES["actions"]["mark_as"]

    def __init__(self):
        """
        Initiates the class instance with variables.
        """
        self.filtered_emails = []
        self.gmail_service = api.get_gmail_service()

    @staticmethod
    def get_message_label_object() -> Dict:
        """Retuns an empty label object structure."""
        return {
            'removeLabelIds': [],
            'addLabelIds': []
        }

    def mark_read_unread(self, label):
        """
        Marks the filtered emails as Read/Unread based on the user choice.
        :param label: READ/UNREAD - based on user choice.
        :return: None
        """

        message_label_obj = {**self.get_message_label_object()}
        all_message_ids = []
        for email in self.filtered_emails:
            label_list: List = email['label'].split(',')
            all_message_ids.append(email["message_id"])
            if label == "READ":
                if "UNREAD" in label_list:
                    label_list.remove("UNREAD")
                    message_label_obj["removeLabelIds"].append("UNREAD")
                    email['is_read'] = True
                    _label = ",".join(label_list)
                    email['label'] = label_list
                    core.update_email_label(message_id=email["message_id"], label=_label)
            elif label == "UNREAD":
                if "UNREAD" not in label_list:
                    label_list.append(label)
                    message_label_obj["addLabelIds"].append("UNREAD")
                    email['is_read'] = False
                    _label = ','.join(label_list)
                    email['label'] = label_list
                    core.update_email_label(message_id=email["message_id"], label=_label)
            core.update_email_status(message_id=email["message_id"], label=label)
        message_label_obj["ids"] = all_message_ids
        api.modify_message(msg_labels=message_label_obj)

    def archive_mail(self):
        """
        Archives the filtered emails.
        :return:None
        """
        message_label_obj = self.get_message_label_object()
        all_message_ids = []
        for email in self.filtered_emails:
            all_message_ids.append(email["message_id"])
            label_list: List = email['label'].split(',')
            if "INBOX" in label_list:
                label_list.remove("INBOX")
                message_label_obj["removeLabelIds"].append("INBOX")
            label = ",".join(label_list)
            email['label'] = label
            email['is_archived'] = True
            core.update_email_label(message_id=email["message_id"], label=label)
            core.change_archive_status(message_id=email["message_id"], status=True)
            message_label_obj["ids"] = all_message_ids
        api.modify_message(msg_labels=message_label_obj)

    def add_custom_label(self, custom_label: str):
        """
        Add custom user label to the email object.
        Change label in database and in Gmail.
        :param custom_label: Label to add.
        :type custom_label: str
        :return: None
        """
        user_labels = api.list_labels(service=api.get_gmail_service(), user_id='me')
        all_labels = [label['name'] for label in user_labels]
        if custom_label.upper() in all_labels:
            label_dict = user_labels[all_labels.index(custom_label.upper())]
            message_label_obj = {
                'removeLabelIds': [],
                'addLabelIds': [label_dict["id"]]
            }
            all_message_ids = []
            for email in self.filtered_emails:
                all_message_ids.append(email["message_id"])
                label_list: List = email['label'].split(',')
                if custom_label.upper() not in label_list:
                    label_list.append(custom_label.upper())
                label = ','.join(label_list)
                core.update_email_label(message_id=email["message_id"], label=label)
                message_label_obj["ids"] = all_message_ids
                email['label'] = label
            api.modify_message(msg_labels=message_label_obj)
        else:
            label = self.create_custom_label(label_name=custom_label.upper())
            message_label_obj = {
                'removeLabelIds': [],
                'addLabelIds': [label["id"]]
            }
            all_message_ids = []
            for email in self.filtered_emails:
                all_message_ids.append(email["message_id"])
                label_list: List = email['label'].split(',')
                if custom_label.upper() not in label_list:
                    label_list.append(custom_label.upper())
                label = ','.join(label_list)
                core.update_email_label(message_id=email["message_id"], label=label)
                message_label_obj["ids"] = all_message_ids
                email['label'] = label
            api.modify_message(msg_labels=message_label_obj)

    def create_custom_label(self, label_name: str):
        """
        Create custom user labels using the Gmail API.
        :param label_name: Label name to create.
        :return: Label object from the Gmail API.
        """
        label_object = api.make_label(label_name=label_name)
        label = api.create_label(service=self.gmail_service, user_id='me', label_object=label_object)
        return label

    def perform_action(self, action: str):
        """
        Maps the action with its function reference.
        :param action: Action to perform on the filtered emails.
        :return: Reference of the function specified.
        """
        return {
            "mark_as": self.mark_read_unread,
            "archive": self.archive_mail,
            "add_label": self.add_custom_label
        }[action]
