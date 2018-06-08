import contextlib2
from urllib.parse import urlencode
from urllib.request import urlopen


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' +
                   urlencode({'url':url}))
    with contextlib2.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')

