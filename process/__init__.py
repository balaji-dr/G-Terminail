"""
This package contains modules to process the stored emails
from the local database. Contains four main files.

core.py -> Contains functions that directly interacts with database.
All the database interactions are in a single file which makes caching
at a later stage will be an easy task.

composed.py -> Contains functions that parses the database objects.

printinfo.py -> Contains functions that prints the menu and extracted data.

manager.py -> Contains classes to process the rules and perform actions
on the extracted emails.
"""
