import os
from typing import Dict
import json
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Can be changed based on the number of emails requirement.
# Can be further used for pagination purpose since the maximum number of
# emails that can be fetched in one request is 100.
MAX_RESULTS_PER_PAGE = 10  # Keep it below 20 for faster response

# Total number of pages to read from gmail.
TOTAL_PAGES_TO_READ = 4

# This will create new database for testing purpose.
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
