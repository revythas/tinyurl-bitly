from flask import Blueprint, jsonify, request
from werkzeug.local import LocalProxy
from flask import current_app
from .tinyurl import Tinyurl
from .bitly import Bitly

api = Blueprint('api', __name__)
logger = LocalProxy(lambda: current_app.logger)

@api.route('/shortlinks/', methods=['POST'])
@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    content = request.get_json()
    response = {'url':'0', 'link':'0'}
    if 'url' in content:
        # Default provider
        providers = ['tinyurl', 'bitly']
        provider = ''
        if 'provider' in content:
            if content['provider'] in providers:
                provider = content['provider']
            else:
                logger.debug('Provider is not supported. Using tinyurl as the default')
                provider = 'tinyurl'
        if provider == '' or provider == 'tinyurl':
            if provider == '':
                logger.debug('Using tinyurl as the default')
            tiny = Tinyurl()
            status, short_link = tiny.call_tiny(content['url'], logger)
            if status != 200:
                logger.debug('TinyURL failed. Falling back to bitly provider')
                bitly = Bitly()
                status, short_link = bitly.call_bitly(content['url'], logger)
                if status != 200:
                    logger.debug('Give up. None method could be processed')
                    return jsonify({'error':'HTTP status : {}'.format(status)})
        elif provider == 'bitly':
            bitly = Bitly()
            status, short_link = bitly.call_bitly(content['url'], logger)
            if status != 200:
                tiny = Tinyurl()
                status, short_link = tiny.call_tiny(content['url'], logger)
                if status != 200:
                    logger.debug('Give up. None method could be processed')
        response['url'], response['link'] = content['url'], short_link
        return jsonify(response)
    else:
        return jsonify({'error':'You have to submit a valid JSON which has a valid provider'})
