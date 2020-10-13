from os.path import abspath, dirname
from requests import Response

MY_PATH = abspath(dirname(__file__)) + '/'
MY_FILE_NAME = 'cookies.json'


class BaseHook:

    def __init__(self, file=None, path=None):
        self.r: Response = ...
        self.kwargs: dict = {}
        self.file = (path or MY_PATH) + (file or MY_FILE_NAME)

    def __call__(self, r, **kwargs):
        self.r = r
        self.kwargs = kwargs
        self.run()

    def run(self):
        pass
