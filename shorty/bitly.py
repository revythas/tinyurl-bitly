import requests

class Bitly:

    def call_bitly(self, long_url, logger):
        token = '<YOUR_TOKEN>'
        header = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json'
        }
        params = {
            'long_url': long_url
        }
        try:
            response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=params, headers=header)
            data = response.json()
            if 'link' in data.keys(): 
                short_link = data['link']
            else: 
                short_link = None
        except Exception as ex:
            logger.error('Exception occured : {}'.format(ex))
            raise
        return response.status_code, short_link
