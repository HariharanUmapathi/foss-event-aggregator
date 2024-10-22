from bs4 import BeautifulSoup

from data_extractors.extractor import Extractor, ExtractorDetail
from data_extractors.util import get_response

EXTRACTOR = ExtractorDetail(
    name="ICFOSS Extractor",
    url="https://icfoss.in/events",
    params="?page=1",
)


class ICFOSSExtractor(Extractor):
    def __init__(self):
        self.name = EXTRACTOR.name
        self.url = EXTRACTOR.url
        self.params = EXTRACTOR.params

    @staticmethod
    def get_extractor_detail():
        return EXTRACTOR

    def collect_data(self):
        # Function to scrape data from https://icfoss.in/events

        event_page_url = self.url + self.params
        data = []

        while True:
            response = get_response(url=event_page_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                for event_day_selector in soup.select(".event_block"):
                    event = {}
                    date_css = ".event_block_header"
                    event["start_date"] = event_day_selector.select_one(date_css).get_text()
                    event["end_date"] = event["start_date"]

                    for event_selector in event_day_selector.select(".event_single"):
                        heading = event_selector.select_one("h3 a")
                        event["title"] = heading.get_text()
                        event["url"] = heading.get("href") or ""
                        venue_css = ".event_venue span"
                        event["location"] = event_selector.select_one(venue_css).get_text()
                        data.append(self.clean_event(event))

                if not (next_page_selector := soup.select_one("[rel='next']")):
                    break

                if not (next_page_url := next_page_selector.get("href")):
                    break

                event_page_url = next_page_url

        return data

    def clean_event(self, event):
        return {attribute_key: event[attribute_key].strip() for attribute_key in event}
