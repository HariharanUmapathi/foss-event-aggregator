"""
Data Extractor Implementation Notes : 
The Data Extractor you're creating is responsible for collecting the event information form the website
to the python dictionary format to store data you can use n numberof function you need inside the 
python class it should override the collectdata method should 

"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

class Extractor(ABC):

    @abstractmethod
    def collect_data(self):
        pass

class ExtractorDetail():
    url: str
    name: str
    params: str