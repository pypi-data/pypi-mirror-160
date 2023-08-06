import requests
import simplejson as json

from .lld import Loader
from .urls import Url

class Repo:
    _repos_data = None
    _terminal_logs = None

    def __init__(self, terminal_logs):
        self._terminal_logs = terminal_logs

    def _repo_jdata_init(self, _count, username):
        if len(self._repos_data) >= _count: return
        if self._terminal_logs: loader = Loader("Loading Repositories Data...", 0.08, 'Repositories loaded!').start()
        url = Url['repo'].value.format(username, _count)
        self._repos_data = json.loads((requests.get(url)).text)
        if self._terminal_logs: loader.stop()
