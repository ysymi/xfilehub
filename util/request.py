import logging
import urllib.parse
import urllib.request


def do_request(url, host='localhost', port=80, ):
    uri = 'http://%s:%s%s' % (host, port, url)
    request = urllib.request.Request(uri)
    try:
        response = urllib.request.urlopen(request)
        response = response.read()
        return response
    except Exception as e:
        logging.exception('%s' % str(e))
        return None
