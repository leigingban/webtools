import re

from ext_app.webtools import Session
from ext_app.webtools.hooks import CookieSavingHook

session = Session()
session.hooks = {'response': [CookieSavingHook()]}
resp = session.get('https://smzdm.com')
resp = session.get('http://httpbin.org/cookies/set/test/test')
# print(session.cookies)
# print(resp)


# a = 'https://www.smzdm.com/'
# b = 'https://m.smzdm.com/'
# c = 'http://httpbin.org/cookies/set/test/test'
#
# pattern = r'\/\/(.*)\/'
# aa = re.findall(pattern, a)
# print(aa)
