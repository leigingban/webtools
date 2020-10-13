import json
import re
from json import JSONDecodeError

from ext_app.webtools.hooks import BaseHook


class CookieSavingHook(BaseHook):

    def __init__(self, file=None, path=None):
        super().__init__(file, path)

    def run(self):
        if cookie := self.r.headers.get('Set-Cookie'):

            cookie_new = self.cookies_from_response(cookie)
            # 域名 + 目录作为唯一索引，方便进行更新替代
            uni_cookies_name = cookie_new.get('Domain') + cookie_new.get('Path')

            cookies_org = self.load_cookies_from_file()
            cookies_org.update({uni_cookies_name: cookie_new})
            self.save_cookies_to_json(cookies_org)

        else:
            pass

    @property
    def domain(self) -> str:
        return re.findall('//(.*?)/', self.r.url)[0]

    def cookies_from_response(self, cookie: str):
        """
        __ckguid=WS44Xy95cAbHEjgVRAo4Nq2; Max-Age=31536000; Domain=smzdm.com; Path=/; HttpOnly,
        __jsluid_s=8e8770c491de42ddea726d37aa4cb2e2; max-age=31536000; path=/; HttpOnly; secure
        """
        cookie = cookie
        _dict = {}
        _kvs = {}

        for first_items in cookie.split(', '):
            for second_items in first_items.split('; '):
                _kv = second_items.split('=')
                if _kv[0] == "Domain":
                    _dict["Domain"] = _kv[1]
                elif _kv[0] == "Path":
                    _dict["Path"] = _kv[1]
                elif _kv[0] == "max-age":
                    _dict["max-age"] = _kv[1]
                elif _kv[0] == "Expires":
                    _dict["Expires"] = _kv[1]
                elif _kv[0] == "httponly":
                    _dict["httponly"] = True
                elif _kv[0] == "secure":
                    _dict["secure"] = True
                else:
                    if len(_kv) > 1:
                        _kvs.update({_kv[0]: _kv[1]})

        _dict['kvs'] = _kvs
        _dict.setdefault("domain", self.domain)

        return _dict

    def load_cookies_from_file(self):
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            if isinstance(e, FileNotFoundError) or isinstance(e, JSONDecodeError):
                print('无法读取数据，数据未初始化！')
                return {}
        return data

    def save_cookies_to_json(self, data):
        try:
            with open(self.file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(e)
