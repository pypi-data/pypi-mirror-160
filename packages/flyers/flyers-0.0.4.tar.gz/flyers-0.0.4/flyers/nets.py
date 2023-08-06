import requests
from requests import Response

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 ' \
             'Safari/537.36 '


class ProxyType(object):
    SOCKS5 = 'SOCKS5'
    HTTP = 'HTTP'


def http_get(url, params=None, **kwargs) -> Response:
    if 'headers' in kwargs:
        kwargs['headers']['User-Agent'] = USER_AGENT
    else:
        kwargs['headers'] = {'User-Agent': USER_AGENT}
    return requests.get(url, params, **kwargs)


def build_proxies(proxy_type=ProxyType.HTTP, host='127.0.0.1', port=1080) -> dict:
    proxy_url = '{}:{}'.format(host, port)
    if proxy_type == ProxyType.HTTP:
        proxy = {
            "http": "http://{}".format(proxy_url),
            "https": "https://{}".format(proxy_url)
        }
    elif proxy_type == ProxyType.SOCKS5:
        proxy = {
            "http": "socks5://".format(proxy_url),
            "https": "socks5://{}".format(proxy_url)
        }
    else:
        raise TypeError('The value of type only has two types: socks5 and http, see ProxyType class')
    return proxy


def download(url: str, filename: str) -> None:
    b = requests.get(url).content
    with open(filename, 'wb+') as f:
        f.write(b)
