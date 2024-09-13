from dataextractors.Extractor import Extractor
from datetime import datetime
import requests,xml.etree.ElementTree as ET 
class FossForceExtractor(Extractor):
        def __init__(self):
            super().__init__()
            self.name="FossForceExtractor"
            self.url = "https://fossforce.com"
            self.params = f"""?feed=event_feed&search_keywords&search_location&search_datetimes=%7B"start"%3A"1-1-2024"%2C"end"%3A"12-31-2024"%7D&search_categories&search_event_types&search_ticket_prices"""
        def collectdata(self)->list:
             eventlist = []
             print("Initializing the data fetch")
             response = requests.get(self.url+self.params)
             if response.status_code ==200:
                try:
                    with open('temp.xml',"wb") as temp_xml:
                         temp_xml.write(response.content)
                         print("writing temporary xml")  
                    temp_xml = open("temp.xml","rb")          
                    xml_payload_size= len(temp_xml.read())
                    if xml_payload_size > 0 :
                        print(f"Size of xml payload:{xml_payload_size}")
                        xmltree=ET.parse("temp.xml")
                        root  = xmltree.getroot()

                        for child in root.iter('item'):
                            event ={}
                            event['title'] = child.find('title').text
                            event['start_date'] = child.find('pubDate').text
                            event['end_date'] = child.find('pubDate').text
                            try:
                                event['description'] = child.find('description').text
                            except AttributeError:
                                 event['description'] = ''
                            event['url'] = child.find('link').text
                            eventlist.append(event)
                        return eventlist
                    else:
                        raise ValueError('XML Not Written')
                    
                except ET.ParseError as err:
                     print("parse error occured")

