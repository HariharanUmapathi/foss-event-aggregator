from dataextractors.Extractor import Extractor
import requests,lxml.html,json
class FossEventsExtractor(Extractor):
    def __init__(self):
        super().__init__()
        self.name="Constructor"
        self.url = "https://foss.events/"
    def collectdata(self)->list:
        # function to scrape event details from the https://foss.events/
        response = requests.get(self.url)
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
            return data
        else:
            return []