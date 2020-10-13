import json
from json import JSONDecodeError

from requests.cookies import RequestsCookieJar

from ext_app.webtools.hooks import MY_PATH, MY_FILE_NAME


def cookies_dict_from_json():
    try:
        with open(MY_PATH + MY_FILE_NAME, 'r') as f:
            data = json.load(f)
    except Exception as e:
        if isinstance(e, FileNotFoundError) or isinstance(e, JSONDecodeError):
            print('无法读取数据，数据未初始化！')
            return None
    return data


def cookie_jar_from_json():
    jar = RequestsCookieJar()
    cookies: dict = cookies_dict_from_json()
    if cookies is None:
        return jar
    for k, v in cookies.items():  # k - (domain + path), v - (dict)
        for name, value in v.get('kvs').items():
            _rest = {'HttpOnly': None} if v.get('httponly') else {}
            jar.set(name, value, domain=v.get('Domain'), path=v.get('Path'), secure=v.get('secure'), rest=_rest)

    return jar
