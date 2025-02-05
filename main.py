import filters
import networking
import parser

prompt = """
Please select one of the options:
0 : quit
1 : last week's summary  (csv)
2 : last week's summary  (detailed)
3 : last month's summary (csv)
4 : last month's summary (detailed)
"""

def main():
    # prompt the user for the input, and make sense out of the user input
    user_input = input(prompt)
    duration = ''
    filter = ''
    separate_subtags = ''
    if (user_input == '0'):
        print(":) bye bye!")
        return 0
    elif (user_input == '1'):
        duration = 'week'
        filter = 'csv'
    elif (user_input == '2'):
        duration = 'week'
        filter = 'detailed'
    elif (user_input == '3'):
        duration = 'month'
        filter = 'csv'
    elif (user_input == '4'):
        duration = 'month'
        filter = 'detailed'
    else:
        exit("wrong input!")
        return -1;
    if (filter == "detailed"):
        separate_subtags = input("separate subtags (yes/no): ")
    else:
        separate_subtags = "no"

    # fetch the events
    networking.fetch_calendar_events(duration)

    # create a structure out of the events response
    events_list = parser.parse_xml_events("calendar.xml")
    tagged_events = parser.get_tagged_events(events_list)

    # show the tags and ask for which tag to show the events for
    print("Please choose a tag: ")
    for tag in tagged_events:
        print(f"- {tag}")
    user_tag = input("Input: ")

    # finally apply the filter for that tag
    if (separate_subtags == "yes"):
        filters.apply_filter(tagged_events, user_tag, filter, True)
    elif (separate_subtags == "no"): 
        filters.apply_filter(tagged_events, user_tag, filter, False)
    else:
        print("wrong user input for separate by subtag!")
        exit(-1)


if __name__ == "__main__":
    # run the main function
    main();
