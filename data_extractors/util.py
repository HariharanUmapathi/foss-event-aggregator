import logging
from tenacity import before_log, after_log
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), before=before_log(logger, logging.INFO), after=after_log(logger, logging.INFO))
def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
