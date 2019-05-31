# G-Terminail

A simple Gmail client that runs in your Terminal.

## Description

This is a standalone python script that connects with Gmail API to filter and perform actions on 
the emails based on certain rules. The user can fetch all the emails from their gmail account and store it in the local
database. Filters can be applied on the stored emails and the actions like marking them as READ/UNREAD, Archiving, Adding new labels can be done through the terminal. Basically its a terminal version of Gmail.

### Pre-requisites

```
Python 3.6 above
SQLite
Virtualenv
```

### Installing

Open the terminal.

Clone the repository
```
git clone https://github.com/deeaarbee/G-Terminail
cd G-Terminail
```

Create virtual environment and activate

```
virtualenv -p python3 happyenv
source happyenv/bin/activate
```

Install requirements

```
pip3 install -r requirements.txt
```

Place the client.json file in the gmail directory.

```
cd gmail
# paste the client.json file
```

In the settings.py in the config directory:
 - TOTAL_PAGES_TO_READ - Total pages to read from gmail.
 - MAX_RESULTS_PER_PAGE - Total email per page.
 - TESTING - True to run tests, else False.

```
# set value for 
MAX_RESULTS_PER_PAGE = 10
TOTAL_PAGES_TO_READ = 3
TESTING = False
```


Run main.py

```
python3 main.py
```

The web browser will open for OAuth for Gmail. Accepting it will show the menu in the terminal.

##### Sample terminal output menu:
```
Successfully dumped email to database!
+--------+------------------------+
| CHOICE |        ACTIONS         |
+--------+------------------------+
|   1    | FILTER/PERFORM ACTIONS |
|   2    |    VIEW SINGLE MAIL    |
|   3    |    SYNC WITH GMAIL     |
|   4    |    VIEW ALL EMAILS     |
|   5    |     EXIT (LOGOUT)      |
+--------+------------------------+

```

## Running the tests

To run the test:

Go to settings.py in config directory:
```
# SET
TESTING = True
```

Now in the project root directory:
```
python3 test.py
```

A new test database will be created to perform the tests.

##### NOTE : Never run test with main database. Set TESTING=True.

##### Sample Test output:

```
(happyenv) bash-3.2$ python3 test.py
.....
----------------------------------------------------------------------
Ran 5 tests in 0.038s

OK
```

## Further improvements (Not required for the given tasks.)

* Database schema can be improved to make it scalable and store all fields of an email.
* Dynamic pagination can be added to reduce load time.
* Mock tests for api requests can be written.


## License

None


