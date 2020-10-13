from collections import OrderedDict

import urllib3
from requests import Session as _Session, auth as _auth
from requests.adapters import HTTPAdapter
from requests.models import DEFAULT_REDIRECT_LIMIT, cookiejar_from_dict, Response
from requests.structures import CaseInsensitiveDict


# 当'Accept-Encoding': 'br' 包含br是需要用到此库
# import brotli


def print_set_cookies(r: Response, **kwargs):
    print(r.url, r.status_code, id(r))
    print(kwargs)
    if r.status_code != 301:
        print(r.headers)


class SessionDebugMixin:
    debug_switch = False
    debug_proxy = {
        'http': 'http://127.0.0.1:6152',
        'https': 'http://127.0.0.1:6152'
    }
    errors = []


class Session(_Session):
    """
    自定义Session，修改部分参数已经加入自己常用的功能
    """

    def __init__(self) -> None:
        self.headers = CaseInsensitiveDict({
            'User-Agent': 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Accept-Encoding': ', '.join(('gzip', 'deflate')),
            'Accept': '*/*',
            'Connection': 'keep-alive',
        })
        self.auth = None
        self.proxies = {}

        #: Event-handling hooks.
        # self.hooks = default_hooks()
        # 仅能 hooks response
        self.hooks = {'response': []}
        self.params = {}

        #: Stream response content default.
        self.stream = False

        #: SSL Verification default.
        self.verify = True

        #: SSL client certificate default, if String, path to ssl client
        #: cert file (.pem). If Tuple, ('cert', 'key') pair.
        self.cert = None

        #: Maximum number of redirects allowed. If the request exceeds this
        #: limit, a :class:`TooManyRedirects` exception is raised.
        #: This defaults to requests.models.DEFAULT_REDIRECT_LIMIT, which is
        #: 30.
        self.max_redirects = DEFAULT_REDIRECT_LIMIT

        #: Trust environment settings for proxy configuration, default
        #: authentication and similar.
        self.trust_env = True

        #: A CookieJar containing all currently outstanding cookies set on this
        #: session. By default it is a
        #: :class:`RequestsCookieJar <requests.cookies.RequestsCookieJar>`, but
        #: may be any other ``cookielib.CookieJar`` compatible object.
        self.cookies = cookiejar_from_dict({})

        # Default connection adapters.
        self.adapters = OrderedDict()
        self.mount('https://', HTTPAdapter(max_retries=3))
        self.mount('http://', HTTPAdapter(max_retries=3))


class AutoSaveCookieSession(Session):

    def __init__(self):
        super().__init__()

        from ext_app.webtools.cookie_utils import cookie_jar_from_json
        self.cookies = cookie_jar_from_json()

        from ext_app.webtools.hooks import CookieSavingHook
        self.hooks = {'response': [CookieSavingHook()]}


class DebugSession(Session):
    def __init__(self) -> None:
        super().__init__()

        # urllib3.disable_warnings()
        # self.cert = ('/Volumes/HDD/workplace/rentos/ext_app/webtools/cert.pem',
        #              '/Volumes/HDD/workplace/rentos/ext_app/webtools/key.pem')
        self.cert = '/Volumes/HDD/workplace/rentos/ext_app/webtools/cert_key.pem'
        self.proxies = {
            'http': 'http://127.0.0.1:6152',
            'https': 'http://127.0.0.1:6152'
        }
