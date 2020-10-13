from types import TracebackType
from typing import Optional

from requests import RequestException


class LoginError(RequestException):

    def with_traceback(self, tb: Optional[TracebackType]) -> BaseException:
        return super().with_traceback(tb)
