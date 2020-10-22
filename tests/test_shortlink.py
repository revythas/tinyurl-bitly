import os
import sys
import json

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from shorty.app import create_app


class TestShortlink:
    """
    GIVEN a Flask application configured for testing
    WHEN the '/shortlinks' page is is posted to (POST) for bitly/tinyurl
    THEN check that a '200' status code is returned and also getting a valid JSON
    FALLING back to tinyurl if there is an unkonwn provider
    """
    url = '/shortlinks'
    mimetype = 'application/json'

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    flask_app = create_app({
                    'TESTING': True
                })

    def test_shortlink_bitly(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/shortlinks' page is is posted to (POST) with 'bitly' provider
        THEN check that a '200' status code is returned and also getting a valid JSON
        """
        data = {
            'url': 'http://google.com/test/123',
            'provider': 'bitly'
        }

        with self.flask_app.test_client() as test_client:
            response = test_client.post(self.url, data=json.dumps(data), headers=self.headers)
            assert response.status_code == 200
            assert response.json['url'] == data['url']
            assert response.json['link'] != '' and 'https://bit.ly/' in response.json['link']

    def test_shortlink_tinyurl(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/shortlinks' page is is posted to (POST) with 'tinyurl' provider
        THEN check that a '200' status code is returned and also getting a valid JSON
        """
        data = {
            'url': 'http://google.com/test/123',
            'provider': 'tinyurl'
        }

        with self.flask_app.test_client() as test_client:
            response = test_client.post(self.url, data=json.dumps(data), headers=self.headers)
            assert response.status_code == 200
            assert response.json['url'] == data['url']
            assert response.json['link'] != '' and 'https://tinyurl.com/' in response.json['link']

    def test_shortlink_default(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/shortlinks' page is is posted to (POST) with ???UKNOWN??? provider
        THEN use 'tinyurl' as the default provider and check that a '200' status code is returned and also getting a valid JSON
        """
        data = {
            'url': 'http://google.com/test/123',
            'provider': 'other-provider'
        }

        with self.flask_app.test_client() as test_client:
            response = test_client.post(self.url, data=json.dumps(data), headers=self.headers)
            assert response.status_code == 200
            assert response.json['url'] == data['url']
            assert response.json['link'] != '' and 'https://tinyurl.com/' in response.json['link']
