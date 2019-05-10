from typing import Dict
import json
from model import ROOT_DIR
import operator
from process import composed


class RuleManager:

    string_fields = ["from_address", "to_address", "subject", "message_body", "label", "message_id"]
    date_field = ["received_on", "created_on", "updated_on"]
    date_unit = ["days", "months"]
    rule_dict = {}

    def __init__(self):
        self.rule_predicate = "all"
        self.string_query = {}
        self.string_predicate = {}
        self.all_emails = composed.extract_email_queryset()
        self.filtered_emails = []

    def load_rule_json(self, json_filename: str) -> Dict:
        with open(ROOT_DIR + "/config/" + json_filename) as json_file:
            self.rule_dict = json.load(json_file)
        json_file.close()
        return self.rule_dict

    @staticmethod
    def rule_predicate_converter(predicate):
        return {
            "all": operator.and_,
            "any": operator.or_
        }[predicate]

    @staticmethod
    def predicate_converter(predicate):
        return {
            "contains": operator.contains,
            "does_not_contain": operator.not_(operator.contains),
            "equals": operator.eq,
            "does_not_equal": operator.is_not,
            "less_than": operator.lt,
            "greater_than": operator.gt
        }[predicate]

    def process_operation(self, operand1, operation, operand2):
        return self.predicate_converter(operation)(operand1, operand2)

    def apply_filters(self):
        for email in self.all_emails:
            for field, predicate in self.string_predicate.items():
                if self.process_operation(operand1=email.get(field),
                                                 operation=predicate,
                                                 operand2=self.string_query.get(field)):
                    if self.rule_predicate == "any":
                        self.filtered_emails.append(email)
                        break
                    elif self.rule_predicate == "all":
                        continue
                else:
                    if self.rule_predicate == "all":
                        break
                    elif self.rule_predicate == "any":
                        continue
                self.filtered_emails.append(email)
