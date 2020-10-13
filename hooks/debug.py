import json

from ext_app.webtools.hooks import BaseHook


class ShowDebugMsgHook(BaseHook):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = ''

    def run(self):
        print(self.r.url, json.loads(self.r.request.body), self.r.status_code, self.r.reason, self.r.elapsed)