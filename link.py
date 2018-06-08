import contextlib2
from urllib.parse import urlencode
from urllib.request import urlopen


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' +
                   urlencode({'url':url}))
    try:
        with contextlib2.closing(urlopen(request_url)) as response:
            return response.read().decode('utf-8')
    except IOError:
        print('error')
    return url

