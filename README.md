# foss event aggregator
Foss Event aggregator is a CLI which is going to create ICalendar(.ics) file to import the events data to our local calendar or google calendar about the events form the following sites 

## Events Sources 
The following websites are our current event sources 
- https://foss.events/
- https://fossforce.com/events-calendar/
- https://fossunited.org/events/timeline
- 
## ICS Generation Code - from Medium 
https://medium.com/simform-engineering/effortless-event-management-with-ics-files-sync-code-and-schedule-b5c62d08d6b5

## Packages we are going to use 
- argparse
- lxml (or) beautifulsoup for web scrapping

## Structure of event we are going to create ics file
Event 
  - title : (mandatory) title of the event to represent in calendar
  - url : (mandatory)
  - startDate: event start date
  - endDate: event end date (start date and end date can be same if oneday event) 
  - description : (optional)
  - location : (optional)
  
## Contributing

if you find a additional sites to collect the event details reference kindly create a issue 
