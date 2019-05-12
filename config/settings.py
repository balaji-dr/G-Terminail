import os
from typing import Dict
import json
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Can be changed based on the number of emails requirement.
# Can be further used for pagination purpose.
MAX_RESULTS_PER_PAGE = 10
TOTAL_PAGES_TO_READ = 2

TESTING = False


def load_rule_json(json_filename: str) -> Dict:
    """
    Load the json file.
    :param json_filename: Name of the json rule file.
    :type json_filename: str
    :return: Rule dictionary.
    :rtype: dict
    """
    with open(ROOT_DIR + "/" + json_filename, 'r') as json_file:
        rule_dict = json.load(json_file)
    json_file.close()
    return rule_dict


RULES = load_rule_json(json_filename="rules.json")
