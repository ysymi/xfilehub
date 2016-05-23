import json
import logging
import urllib.parse
import urllib.request


def do_request(uri, host='localhost', port=80, to_dict=False):
    url = 'http://%s:%s%s' % (host, port, uri)
    logging.info('url: %s' % url)
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        response = response.read().decode('utf-8')
        logging.info(response)
        if to_dict:
            response = json.loads(response)

        return response
    except Exception as e:
        logging.exception('%s' % str(e))
        return None
