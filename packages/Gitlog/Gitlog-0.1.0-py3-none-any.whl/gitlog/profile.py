import requests
import simplejson as json

from gitlog.lld import Loader
from gitlog.urls import Url


class Profile:
    id = None
    username = None
    fullname = None
    profile_url = None
    avatar_url = None
    _profile_data = None
    _terminal_logs = None

    def __init__(self, username, fullname, profile_url, avatar_url, terminal_logs):
        self._terminal_logs = terminal_logs
        self.username = username
        if fullname or profile_url or avatar_url is None:
            self._prof_jdata_init()
            try:
                self.id = self._profile_data['id']
                self.fullname = self._profile_data['name']
                self.avatar_url = self._profile_data['avatar_url']
                self.profile_url = self._profile_data['url']
            except KeyError as kerr:
                raise RuntimeError('Username \'{}\' not found!'.format(username)) from kerr

    def _prof_jdata_init(self):
        if self._profile_data is not None: return
        if self._terminal_logs: loader = Loader("Loading Profile Data...", 0.08, 'Profile loaded!').start()
        url = Url['user'].value.format(self.username)
        self._profile_data = json.loads((requests.get(url)).text)
        if self._terminal_logs: loader.stop()
