import urllib
import requests

class Tinyurl:

    def call_tiny(self, long_url, logger):
        URL = "http://tinyurl.com/api-create.php"
        try:
            url = URL + "?" + urllib.parse.urlencode({"url": long_url})
            short_link = requests.get(url)
            return short_link.status_code, short_link.text
        except Exception as ex:
            logger.error('Exception occured : {}'.format(ex))
            raise