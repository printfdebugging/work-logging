import textwrap

def apply_filter(tagged_events, tag, filter, separate_subtags=False):
    if (filter == "csv"):
        apply_csv_filter(tagged_events, tag)
    elif filter == "detailed":
        apply_detailed_filter(tagged_events, tag, separate_subtags)
    else:
        print("filter not found")
        exit(-1)

def create_nested_subtags_dict(tagged_events):
    # Create a nested dictionary for tags and subtags
    nested_events = {}
    for tag, events in tagged_events.items():
        nested_events[tag] = {}
        for event in events:
            summary_parts = event['SUMMARY'].split(' - ', 1)
            if len(summary_parts) == 2:
                subtag, summary = summary_parts
                event['SUMMARY'] = summary
                if subtag not in nested_events[tag]:
                    nested_events[tag][subtag] = []
                nested_events[tag][subtag].append(event)
    return nested_events

def apply_csv_filter(tagged_events, tag):
    nested_events = create_nested_subtags_dict(tagged_events)
    events = nested_events[tag]

    # Collect all events with their subtags
    all_events = [(subtag, event) for subtag, subtag_events in events.items() for event in subtag_events]
    all_events = sorted(all_events, key=lambda event: (event[1]["DTSTART"], event[1].get("DURATION", 0)))
    aggregate_duration = sum(event.get('DURATION', 0) for _, event in all_events)
    print(f"'{tag}', {aggregate_duration} hours")
    for subtag, event in all_events:
        print(event.get('DTSTART', 'No start date available'), end=",") # start date
        print(f"{event.get('DURATION', 'No duration available')}", end=",") # duration
        print(f"[{subtag}] " + event.get('SUMMARY', 'No summary available'), end=",") # summary
        description = event.get('DESCRIPTION', '- No description available')
        description = description.replace("  ", " ").replace(",", "..").replace("\n", " ").replace("-", "")
        print(description)

def apply_detailed_filter(tagged_events, tag, separate_subtags):
    nested_events = create_nested_subtags_dict(tagged_events)
    events = nested_events[tag]

    if separate_subtags:
        # Print details grouped by subtag
        for subtag, subtag_events in events.items():
            aggregate_duration = sum(event.get('DURATION', 0) for event in subtag_events)
            print("============SUBTAG==================", end="")
            print(f"\nSubtag: {subtag}")
            print(f"Aggregate Duration: {aggregate_duration} hours")
            print("====================================")
            for event in subtag_events:
                print("----------------------------------------------------")
                print("Summary:", end=" ")
                print(event.get('SUMMARY', 'No summary available'))
                print("Duration:", end=" ")
                print(f"{event.get('DURATION', 'No duration available')} hours")
                print("Start Date:", end=" ")
                print(event.get('DTSTART', 'No start date available'))
                print("Description:")
                description = event.get('DESCRIPTION', '- No description available')
                for line in description.split('\n'):
                    wrapped_lines = textwrap.wrap(line, width=60, subsequent_indent='  ')
                    for wrapped_line in wrapped_lines:
                        print(wrapped_line)
    else:
        # Collect all events with their subtags
        all_events = [(subtag, event) for subtag, subtag_events in events.items() for event in subtag_events]
        aggregate_duration = sum(event.get('DURATION', 0) for _, event in all_events)
        print(f"\nAggregate Duration for tag '{tag}': {aggregate_duration} hours")
        for subtag, event in all_events:
            print("------------------------------------------------------")
            print(f"Summary: {subtag} - ", end="")
            print(event.get('SUMMARY', 'No summary available'))
            print("Duration:", end=" ")
            print(f"{event.get('DURATION', 'No duration available')} hours")
            print("Start Date:", end=" ")
            print(event.get('DTSTART', 'No start date available'))
            print("Description:")
            description = event.get('DESCRIPTION', '- No description available')
            for line in description.split('\n'):
                wrapped_lines = textwrap.wrap(line, width=60, subsequent_indent='  ')
                for wrapped_line in wrapped_lines:
                    print(wrapped_line)
