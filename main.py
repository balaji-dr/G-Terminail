from gmail import dump_to_db
from process import composed
from process.manager import RuleManager

# dump_to_db.email_list_to_database()
# composed.print_n_emails(n=5)

running = True

while running:
    manager = RuleManager()
    manager.load_rule_json("rules.json")

    composed.print_rule_predicate()
    choice = input("Enter choice: ")
    if choice == 'q':
        print("Good Bye :)")
        break
    if 0 < int(choice) < 3:
        manager.rule_predicate = RuleManager.rule_dict["rule_predicate"][int(choice)-1]
    while True:
        composed.print_string_fields()
        choice1 = int(input("Enter choice: "))

        if choice1 == 5:
            composed.print_date_units()
            choice3 = int(input("Enter choice: "))
            manager.date_unit = manager.date_unit_list[choice3-1]

            composed.print_date_predicates()
            choice2 = int(input("Enter choice: "))
            manager.predicate_dict[manager.all_fields[choice1-1]] = \
                manager.rule_dict["date_predicate"]["predicate"][choice2-1]

            query = int(input("Enter day/month difference: "))
            manager.query_dict[manager.all_fields[choice1-1]] = query
        else:
            composed.print_field_predicates()
            choice2 = int(input("Enter choice: "))
            manager.predicate_dict[manager.all_fields[choice1 - 1]] = \
                manager.rule_dict["string_predicate"][choice2 - 1]

            query = input("Enter the query string: ")
            manager.query_dict[manager.all_fields[choice1 - 1]] = query

        print("Enter 'a' to add another rule")
        if 'a' == input():
            continue
        else:
            break

    # print(manager.query_dict)
    # print(manager.predicate_dict)
    # print(manager.date_unit)
    # print(manager.rule_predicate)

    manager.apply_filters()
    print(composed.print_n_emails(emails=manager.filtered_emails))


    break
