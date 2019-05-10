from gmail import dump_to_db
from process import composed
from process.manager import RuleManager

# dump_to_db.email_list_to_database()
# composed.print_n_emails(n=5)

running = True

while(running):
    print("Select the string fields to query :")
    for index, fields in enumerate(RuleManager.string_fields):
        print(f"{index+1} -> {fields}")
    ind = input()
