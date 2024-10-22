
from data_extractors.foss_events_extractor import FossEventsExtractor
from data_extractors.foss_force_extractor import FossForceExtractor
from data_extractors.icfoss_extractor import ICFOSSExtractor
AVAILABLE_EXTRACTORS = {
    "FOSS_EVENTS": FossEventsExtractor,
    "FOSS_FORCE": FossForceExtractor,
    "ICS_FOSS":ICFOSSExtractor
}

class ExtractorFactory:

    @staticmethod
    def get_available_extractors():
        return AVAILABLE_EXTRACTORS
    
    def get_extractor(self, extractor: str):
        try:
            return AVAILABLE_EXTRACTORS[extractor]
        except Exception as ex:
            raise f"{extractor} not available"
