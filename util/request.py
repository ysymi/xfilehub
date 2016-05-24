import json
import logging
import urllib.parse
import urllib.request


def do_request(uri, host='localhost', port=80, is_file=False, to_dict=False):
    uri = urllib.parse.quote(uri)  # for chinese character
    url = 'http://%s:%s%s' % (host, port, uri)
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        response = response.read()
        if not is_file:
            response = response.decode('utf-8')
        if to_dict:
            response = json.loads(response)

        return response
    except Exception as e:
        logging.exception('%s' % str(e))
        return None
