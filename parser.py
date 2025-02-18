from datetime import datetime
import xml.etree.ElementTree as ET
import pytz

def parse_xml_events(events):
    """Parse the XML file and extract calendar events."""
    tree = ET.parse(events)
    root = tree.getroot()

    namespaces = {
        'D': 'DAV:',
        'CAL': 'urn:ietf:params:xml:ns:caldav'
    }

    all_events = []

    for response in root.findall('D:response', namespaces):
        calendar_data = response.find('.//CAL:calendar-data', namespaces).text
        events = parse_calendar_data(calendar_data)
        all_events.extend(events)

    return all_events

def parse_calendar_data(calendar_data):
    """Parse calendar data and extract events."""
    events = []
    lines = calendar_data.splitlines()
    event = {}
    tzid = None
    in_description = False
    in_summary = False
    description_lines = []
    summary_lines = []

    for line in lines:
        if line.startswith("BEGIN:VEVENT"):
            event = {}
            description_lines = []
            summary_lines = []
            in_description = False
            in_summary = False
        elif line.startswith("END:VEVENT"):
            if 'DTSTART' in event and 'DTEND' in event:
                # Calculate duration
                duration = (event['DTEND'] - event['DTSTART']).total_seconds() / 3600  # duration in hours
                event['DURATION'] = duration
                if description_lines:
                    event['DESCRIPTION'] = ''.join(description_lines).replace('\\n', '\n').replace('\\,', ',')
                if summary_lines:
                    event['SUMMARY'] = ''.join(summary_lines).replace('\\n', '\n').replace('\\,', ',')
                events.append(event)
        elif line.startswith("DTSTART;TZID="):
            tzid = line.split(':')[0].split('=')[1]
            event['DTSTART'] = parse_datetime(line.split(':')[1], tzid)
        elif line.startswith("DTEND;TZID="):
            tzid = line.split(':')[0].split('=')[1]
            event['DTEND'] = parse_datetime(line.split(':')[1], tzid)
        elif line.startswith("SUMMARY:"):
            in_summary = True
            summary_lines.append(line[len("SUMMARY:"):])
        elif line.startswith("DESCRIPTION:"):
            in_description = True
            description_lines.append(line[len("DESCRIPTION:"):])
        elif in_description:
            if line.startswith(" "):
                description_lines.append(line[1:])
            else:
                in_description = False
        elif in_summary:
            if line.startswith(" "):
                summary_lines.append(line[1:])
            else:
                in_summary = False
    return events

def parse_datetime(datetime_str, tzid):
    """Parse the datetime string and convert it to a timezone-aware datetime object."""
    dt = datetime.strptime(datetime_str, '%Y%m%dT%H%M%S')
    timezone = pytz.timezone(tzid)
    return timezone.localize(dt)

def get_tagged_events(events):
    """Organize events into a dictionary with tags as keys."""
    tagged_events = {}

    for event in events:
        if 'SUMMARY' in event:
            summary_parts = event['SUMMARY'].split(' - ', 2)
            if len(summary_parts) == 3:
                tag, subtag, summary = summary_parts
                event['SUMMARY'] = f"{subtag} - {summary}"
                if tag not in tagged_events:
                    tagged_events[tag] = []
                tagged_events[tag].append(event)

    return tagged_events
