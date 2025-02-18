import requests
import credentials
from datetime import datetime, timedelta, timezone

def fetch_calendar_events(duration):
    # calculate the dates to fetch based on duration
    if (duration == "week"):
        delta = 7
    elif (duration == "month"):
        delta = 30
    else:
        print("wrong duration argument!")
        exit(-1)

    start_date = (datetime.now(timezone.utc) - timedelta(days=delta)).strftime("%Y%m%dT%H%M%SZ")
    end_date = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # Define the XML data for the REPORT request
    data = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
        <d:prop>
            <d:getetag />
            <c:calendar-data />
        </d:prop>
        <c:filter>
            <c:comp-filter name="VCALENDAR">
                <c:comp-filter name="VEVENT">
                    <c:time-range start="{start_date}" end="{end_date}" />
                </c:comp-filter>
            </c:comp-filter>
        </c:filter>
    </c:calendar-query>"""

    print("Fetching calendar events from the last week...")

    # Make the REPORT request
    response = requests.request(
        "REPORT",
        credentials.calendar_url,
        data=data,
        headers={
            "Depth": "1",
            "Content-Type": "application/xml"
        },
        auth=(credentials.username, credentials.password)
    )

    # Check the response
    if response.status_code == 207:
        with open("calendar.xml", "w") as file:
            file.write(response.text)
    else:
        response.raise_for_status()
