# work-logging

## Setting up credentials.py File
  + create a file named credentials.py with the email, password and the calendar id.
  + i use `ansible-vault` and `init.sh` to store the encrypted version of the file in this public repository.

```python
username="email"
password="password"
calendar_url="https://dav.mailbox.org/caldav/calendar_url"
```

## Creating Calendar Events
  + the calendar events should be of the format `tag - subtag - summary`
  + the description should be of the format `- point1\n- point2\n- point3\n`, like markdown lists.

## About the Scripts
  + main.py houses the prompt processing code
  + networking.py is responsible for fetching calendar events and creating calendar.xml file
  + parser.py reads calendar.xml line by line and creates a code representation of the events
  + filters.py prints the events from the code representation in either csv or detailed view.
    + there are currently 4 options, csv and detailed view for the last 7 and 30 days each.
