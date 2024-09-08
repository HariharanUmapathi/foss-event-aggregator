import email
from email.mime.base import MIMEBase
import uuid
from datetime import datetime
from icalendar import Calendar, Event, Alarm, vDatetime, vDate
from decouple import config

class ICSGenerator:
    """
    ICSGenerator class generates an ics file.
    """
    filename = "event_invite.ics"
    # events_info 
    def __init__(self, **events_info):
        self.cal = Calendar()        
        self.events_info = events_info
        #self.event = Event()
        #self.send_reminder_before = events_info.get("send_reminder_before", 15)
    
    # YYYY-MM-DD to VDate conversion 
    def convert_to_ical_datetime(self,date_str, time_str=None):
        """
        Converts a date or date-time string to an iCalendar date-time object.
        :param date_str: Date string in the format "YYYY-MM-DD".
        :param time_str: Time string in the format "HH:MM:SS" (optional).
        :return: vDate or vDatetime object.
        """
    # Parse date and time
        if time_str:
        # If time is provided, parse as datetime
            date_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
            return vDatetime(date_time)
        else:
            # If only date is provided, parse as date
            date_time = datetime.strptime(date_str, "%Y-%m-%d").date()
            return vDate(date_time)
    # need to test and remove if not required
    @property
    def calendar_dict(self):
        return {"prodid": "Eventgator", "version": "0.0.1", "method": "REQUEST"}
    # need to test and remove if not required
    @property
    def event_dict(self):
        return {
            "summary": self.event_info.get("subject"),
            "organizer": config("ORGANIZER_EMAIL"),
            "description": self.event_info.get("description"),
            "dtstart": self.event_info.get("start_time"),
            "dtend": self.event_info.get("end_time"),
            "sequence": 1,
            "uid": uuid.uuid4(),
            "status": "confirmed",
            "attendee;ROLE=REQ-PARTICIPANT": self.event_info.get("attendee_emails"),
            "attendee;ROLE=CHAIR": self.event_info.get("mod"),
        }
    # Update my json keys to event properties format
    def _add(self, component, cal_data: dict):
        """component: event or cal"""
        for key, value in cal_data.items():
            component.add(key, value)
        return component
    # alarm code need to check and remove in future 
    def set_alarm(self, event):
        """
        Set a Reminder Alarm before the meeting.
        """
        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", "Reminder")
        if self.send_reminder_before in [0, 5, 15, 30]:
            alarm.add("TRIGGER;RELATED=START", "-PT{0}M".format(self.send_reminder_before))
        if self.send_reminder_before == 60:
            alarm.add("TRIGGER;RELATED=START", "-PT1H")
        if self.send_reminder_before == 120:
            alarm.add("TRIGGER;RELATED=START", "-PT2H")
        if self.send_reminder_before == 720:
            alarm.add("TRIGGER;RELATED=START", "-PT12H")
        if self.send_reminder_before == 1440:
            alarm.add("TRIGGER;RELATED=START", "-P1D")
        if self.send_reminder_before == 10080:
            alarm.add("TRIGGER;RELATED=START", "-P1W")
        event.add_component(alarm)
    #
    def set_ics_data(self):
        # calendar instance created on ICS Generator intialized
        self._add(self.cal, self.calendar_dict)
        # iterating the events
        for event in self.events_info:
            # creating dictionary for ics file 
            event_properties = {
                "uid": uuid.uuid4(),
                "summary":event["name"],
                "dtstart":self.convert_to_ical_datetime(event['start_date'],False),
                "dtend":self.convert_to_ical_datetime(event['end_date'],False),
                "sequence":0,
                "status":"CONFIRMED",
                "description": event['url']
            }
            # Creating Icalander Event Instance
            foss_event = self._add(Event(),event_properties)
            # After creation adding to the calender
            self.cal.add_component(foss_event)
    # ICS Generation for adding to the public calendar    
    def write_ics_file(self,filename='foss_events.ics'):
        self.set_ics_data()
        with open(filename,"wb") as events_ics_file:
            events_ics_file.write(self.cal.to_ical())

    # Inspration code for generating as a email attachment future code         
    def get_ics_content(self):
        self.set_ics_data()
        part = MIMEBase("text", "calendar", method="REQUEST", name=self.filename)
        part.set_payload(self.cal.to_ical())
        email.encoders.encode_base64(part)
        part.add_header("Content-Description", self.filename)
        part.add_header("Content-class", "urn:content-classes:calendarmessage")
        part.add_header("Filename", self.filename)
        part.add_header("Path", self.filename)
        return part