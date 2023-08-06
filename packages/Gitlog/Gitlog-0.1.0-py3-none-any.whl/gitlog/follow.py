import requests
import simplejson as json

from .lld import Loader
from .urls import Url

class Follow:
    _followers_data = None
    _followings_data = None
    _terminal_logs = None

    def __init__(self, terminal_logs):
        self._terminal_logs = terminal_logs

    def _followers_jdata_init(self, _count, username):
        if len(self._followers_data) >= _count: return
        if self._terminal_logs: loader = Loader("Loading Followers Data...", 0.08, 'Followers loaded!').start()
        url = Url['follower'].value.format(username, _count)
        self._followers_data = json.loads((requests.get(url)).text)
        if self._terminal_logs: loader.stop()

    def _followings_jdata_init(self, _count, username):
        if len(self._followings_data) >= _count: return
        if self._terminal_logs: loader = Loader("Loading Followings Data...", 0.08, 'Followings loaded!').start()
        url = Url['following'].value.format(username, _count)
        self._followings_data = json.loads((requests.get(url)).text)
        if self._terminal_logs: loader.stop()