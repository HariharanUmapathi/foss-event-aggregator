import argparse
VERSION = "V 0.0.1"
DESCRIPTION = f"""Event Aggregator {VERSION} 
This Event Aggregator aggregates the events in specific format required for generating the ics file.
"""
# Web Scrapper or data collector methods -- Starts 


# Web Scrapper or data collector methods -- Ends 

# Cli Argument Handlers -- Starts 
def list_sources():
    sources=[
        "https://foss.events/",
        "https://fossforce.com/events-calendar/",
        "https://fossunited.org/events/timeline",
    ]
    print(sources)
    return sources
def list_events():
    print("Listing events from the events sources")
    return 
def update_events():
    print("Updating the latest events lists")
    return 
def generate_ics():
    print("Generating... ICS File")
    return 
# Cli Argument Handlers -- Ends 
## Function map 
FUNCTIONMAP = {
    'list-sources':list_sources,
    'list-events':list_events,
    'update-events':update_events,
    'generate-ics':generate_ics
}

# Main function 
def eventgator():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-c","--command",dest="command",choices=FUNCTIONMAP.keys())
    args = parser.parse_args()
    try: 
        if args.command == None:
            print("No Command Given")
            return parser.print_help()
        FUNCTIONMAP[args.command]()
    except KeyError:
        print("Invalid Command")
        parser.print_help()
    # Main Function Ends 

if __name__=="__main__":
    eventgator()