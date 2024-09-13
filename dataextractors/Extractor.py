"""
Data Extractor Implementation Notes : 
The Data Extractor you're creating is responsible for collecting the event information form the website
to the python dictionary format to store data you can use n numberof function you need inside the 
python class it should override the collectdata method should 

"""
class Extractor(object):
    def __init__(self):
        self.name="Base Extractor"
        self.url =""
        self.description = ""
    def collectdata(self)->dict:
        return {}