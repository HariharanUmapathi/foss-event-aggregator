import argparse
import inspect
import json

from ICSGenerator import ICSGenerator
from data_extractors.extractor_factory import ExtractorFactory

""" 
dynamic import not working so commented create a issue for discussion on it 
import os,importlib
data_extractors = 'dataextractors'
for filename in os.listdir(data_extractors):
    if filename.endswith(".py") and filename != "__init__.py":  # Exclude __init__.py
        module_name = filename[:-3]  # Remove the .py extension
        full_module_name = f"{data_extractors}.{module_name}"  # Full module path
        module = importlib.import_module(full_module_name)
        imported_module.append(module)
        #print(f"Imported {full_module_name}") """

#defining Constants for various purposes
VERSION = "V 0.0.1"
DESCRIPTION = f"""Event Aggregator {VERSION} 
This Event Aggregator aggregates the events in specific format required for generating the ics file.
"""
 
class CLI(object):

    def __init__(self):
        self._extractors = ExtractorFactory.get_available_extractors()
        self.function_map = {
            'list-sources': self.list_sources,
            'list-events': self.list_events,
            'update-events': self.update_events,
            'generate-ics': self.generate_ics
        }

    def list_sources(self):
        sources = set()
        for name, extractor in self._extractors.items():
            try:
                source = extractor.get_extractor_detail().url
                if source != '':
                    sources.add(source)
            except AttributeError as err:
                print(f"{name} {err}")   
        print("Current Event Sources ",sources)         
        return sources

    def list_events(self):
        print("Listing events from the events sources")
        print("Displaying from last update")

    def update_events(self):
        print("Updating the latest events lists")
        masterlist = []
        for name, extractor in self._extractors.items():
            print(f"Extracting Using {name}")
            masterlist += extractor().collect_data()
            print(len(masterlist))
            with open("event_cache.json","w") as event_cache:
                event_cache.write(json.dumps(masterlist))
                event_cache.close()

    def generate_ics(self):
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
 
def eventgator():
    cli = CLI()
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-c","--command",dest="command",choices=cli.function_map.keys())
    args = parser.parse_args()
    try: 
        if args.command == None:
            print("No Command Given")
            return parser.print_help()
        cli.function_map[args.command]()
    except KeyError as err:
        print("Invalid Command",err)
        parser.print_help()

if __name__=="__main__":
    eventgator()