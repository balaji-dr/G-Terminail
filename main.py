from gmail import dump_to_db
from process import composed
from process.manager import RuleManager, ProcessManager

dump_to_db.email_list_to_database()

while True:
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

    manager.apply_filters()
    composed.print_n_emails(emails=manager.filtered_emails)

    process = ProcessManager()
    process.filtered_emails = manager.filtered_emails

    composed.print_actions()
    choice1 = input("Enter choice: ")

    if choice1 == '1':
        composed.print_mark_email_options()
        choice2 = int(input("Enter choice: "))
        process.perform_action(action=process.actions[int(choice1)-1])(process.mark_as_list[choice2-1])

    elif choice1 == '3':
        choice2 = input("Enter new label name: ")
        process.perform_action(action=process.actions[int(choice1)-1])(choice2)

    else:
        print(process.actions[int(choice1)-1])
        process.perform_action(action=process.actions[int(choice1)-1])()

    composed.print_n_emails(emails=process.filtered_emails)

    break
