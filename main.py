"""
The main executable file that starts the program.
"""

from gmail import dump_to_db
from process import composed, printinfo
from process.manager import RuleManager, ProcessManager
from config.settings import RULES


def main() -> None:
    """
    Main function that gets input from the user and
    calls all the other functions.
    :return:
    """
    while True:
        try:
            # Print all mails
            all_emails = composed.extract_email_queryset
            printinfo.print_n_emails(emails=all_emails())

            # Load rules data
            manager = RuleManager()
            manager.rule_dict = RULES
            printinfo.print_rule_predicate()
            choice = input("Enter choice: ")
            if choice not in ['1', '2', 'q']:
                raise IndexError
            if choice == 'q':
                print("Good Bye :)")
                break
            if 0 < int(choice) < 3:
                manager.set_rule_predicate(index=int(choice)-1)

            # Loop to get all rules
            while True:
                printinfo.print_string_fields()
                choice1 = int(input("Enter choice: "))
                field = manager.all_fields[choice1 - 1]
                if choice1 == 5:
                    printinfo.print_date_units()
                    choice3 = int(input("Enter choice: "))
                    manager.set_date_unit(index=choice3-1)

                    printinfo.print_date_predicates()
                    choice2 = int(input("Enter choice: "))

                    predicate = manager.rule_dict["date_predicate"]["predicate"][choice2-1]
                    manager.set_predicate_dict(key=field, value=predicate)

                    query = int(input("Enter day/month difference: "))
                    manager.set_query_dict(key=field, value=query)
                else:
                    printinfo.print_field_predicates()
                    choice2 = int(input("Enter choice: "))

                    string_predicate = manager.rule_dict["string_predicate"][choice2 - 1]
                    manager.set_predicate_dict(key=field, value=string_predicate)

                    query = input("Enter the query string: ")
                    manager.set_query_dict(key=field, value=query)

                print("Enter 'a' to add another rule")
                if 'a' == input():
                    continue
                else:
                    break

            # Apply the rule filters
            manager.apply_filters()
            printinfo.print_n_emails(emails=manager.filtered_emails)

            # Get the Actions
            process = ProcessManager()
            process.filtered_emails = manager.filtered_emails
            printinfo.print_actions()
            choice1 = input("Enter choice: ")
            action = process.actions[int(choice1) - 1]

            # Perform the actions
            if choice1 == '1':
                printinfo.print_mark_email_options()
                choice2 = int(input("Enter choice: "))
                mark_as_value = process.mark_as_list[choice2-1]
                process.perform_action(action=action)(mark_as_value)
            elif choice1 == '3':
                choice2 = input("Enter new label name: ")
                process.perform_action(action=action)(choice2)
            else:
                print(process.actions[int(choice1)-1])
                process.perform_action(action=action)()
            printinfo.print_n_emails(emails=all_emails())

            # Print main menu
            printinfo.print_main_menu()
            choice1 = int(input("Enter choice: "))
            if choice1 == 1:
                continue
            elif choice1 == 2:
                choice1 = int(input("Enter id of the email to view: "))
                printinfo.print_single_message(mail_id=choice1)
            elif choice1 == 3:
                dump_to_db.email_list_to_database()
            elif choice1 == 4:
                printinfo.print_n_emails(emails=composed.extract_email_queryset())
            elif choice1 == 5:
                break
            continue
        except IndexError as e:
            print(f"Invalid choice. Start again...")
            continue


if __name__ == '__main__':
    # call to function to create/sync local db with Gmail
    dump_to_db.email_list_to_database()
    main()
