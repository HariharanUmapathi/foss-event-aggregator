import argparse,requests,lxml.html
import json 
from ICSGenerator import ICSGenerator
#defining Constants for various purposes
VERSION = "V 0.0.1"
DESCRIPTION = f"""Event Aggregator {VERSION} 
This Event Aggregator aggregates the events in specific format required for generating the ics file.
"""
EVENTTEMPLATE = {
    "title":"",
    "startDate":"",
    "endDate":"",
    "url":"",
    "description":""
}
# Web Scrapper or data collector methods -- Starts 
def foss_events():
    # function to scrape event details from the https://foss.events/
    response = requests.get("https://foss.events/")
    if response.status_code == 200:
        print("lxml html tree building")
        doc_root = lxml.html.fromstring(response.content)
        tables = doc_root.xpath("/html/body/div/table[*]/tr[*]")
        data=[]
        i=0
        for tr in tables:
            event = {}
            event['url'] =tr.xpath('//link[@itemprop="url"]/@href')[i]
            event['start_time']=tr.xpath('//meta[@itemprop="startDate"]/@content')[i]
            event['end_time']=tr.xpath('//meta[@itemprop="endDate"]/@content')[i]
            event['name'] = tr.xpath('//span[@itemprop="name"]/text()')[i].strip()
            #event['language'] = tr.xpath('//span[@itemprop="inLanguage"]/text()')[i]
            #event['organizer'] =tr.xpath('//span[@itemprop="organizer"]//span[@itemprop="name"]/text()')[i]
            #event['cfp_deadline'] = tr.xpath('//p[@class="eventcfp"]/text()')[i+1].strip()
            i=i+1
            data.append(event)
            with open("event_cache.json","w") as event_cache:
                event_cache.write(json.dumps(data))
            event_cache.close()
    else:
        return []
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
#Method should implement
def list_events():
    print("Listing events from the events sources")
    print("Displaying from last update")
    return 
def update_events():
    print("Updating the latest events lists")
    eventslist =[foss_events()]
    print(eventslist)
    return 
def generate_ics():
    print("Generating... ICS File")
    with open("event_cache.json","r") as event_cache:
        json_string  = event_cache.read()
        events = json.loads(json_string)
        print("Events Available : ",len(events))
        print("writing events")
        icsgenerator = ICSGenerator()
        icsgenerator.events_info=events
        icsgenerator.write_ics_file()
        print("ICS File writing done")
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
    except KeyError as err:
        print("Invalid Command")
        parser.print_help()
    # Main Function Ends 

if __name__=="__main__":
    eventgator()