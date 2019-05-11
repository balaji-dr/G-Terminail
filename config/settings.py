import os
from typing import Dict
import json


MAX_RESULTS_PER_PAGE = 10
TOTAL_PAGES_TO_READ = 2
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_rule_json(json_filename: str) -> Dict:
    with open(ROOT_DIR + "/" + json_filename, 'r') as json_file:
        rule_dict = json.load(json_file)
    json_file.close()
    return rule_dict


RULES = load_rule_json(json_filename="rules.json")
