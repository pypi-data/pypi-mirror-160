import queue
import threading
from datetime import datetime
from typing import Any

from .follow import Follow
from .profile import Profile
from .repo import Repo


class User(Follow, Repo, Profile):
    """
    Use this class to get a Github user information such as repositories info,
     follower or following, etc.
    The class User includes parent classes:
        - Follow
        - Repo
        - Profile
    """
    username = None

    def __init__(self, username: str, fullname=None, profile_url=None, avatar_url=None, terminal_logs=True) -> None:
        """
        :param username: Github username in form of string
        OPTIONALS: just pass them if you have them to avoid extra api requests.
        :param fullname: Github user's full name
        :param profile_url: user profile url in form of string
        :param avatar_url: user avatar url in form of string
        :param terminal_logs: terminal logs will print every actions inside
                              the terminal default is True
        """
        Profile.__init__(self, username, fullname, profile_url, avatar_url, terminal_logs)
        Repo.__init__(self, terminal_logs)
        Follow.__init__(self, terminal_logs)
        self.username = username
        self._repos_data, self._followers_data, self._followings_data = [], [], []

    def get_bio(self) -> str:
        """
        :return: user's biography
        """
        return self._profile_data['bio']

    def get_followers_count(self) -> int:
        """
        :return: user's followers count
        """
        return int(self._profile_data['followers'])

    def get_followings_count(self) -> int:
        """
        :return: user's followings count
        """
        return int(self._profile_data['following'])

    def get_created_date(self) -> datetime:
        """
        :return: user's account creation date in form of date and time object e.g. 2020-01-02T10:06:09Z
        """
        return datetime.strptime(self._profile_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')

    def get_location(self) -> str:
        return self._profile_data['location']

    def get_repos(self, *keys, count=100) -> list[dict]:
        if len(keys) == 0:
            keys=['name', 'description']
        self._repo_jdata_init(count, self.username)
        repos, _cc = [], 0
        for repo in self._repos_data:
            if _cc == count: break
            try:
                repos.append({key: repo[key] for key in keys})
            except KeyError as ky_err:
                raise RuntimeError('Key {} is invalid for repository info!'.format(ky_err))
            _cc += 1
        return repos

    def get_followers(self, count=100, _q=None) -> list[Any]:
        self._followers_jdata_init(count, self.username)
        _res_fo = [data['login'] for data in self._followers_data][:count]
        if isinstance(_q, queue.Queue): _q.put(_res_fo)
        else: return _res_fo

    def get_followings(self, count=100, _q=None) -> list[Any]:
        self._followings_jdata_init(count, self.username)
        _res_fo = [data['login'] for data in self._followings_data][:count]
        if isinstance(_q, queue.Queue): _q.put(_res_fo)
        else: return _res_fo

    def _get_follow_data(self, count) -> tuple[Any, Any]:
        _qfg, _qfr = queue.Queue(), queue.Queue()
        _tfg = threading.Thread(target=self.get_followings, args=(count, _qfg))
        _tfr = threading.Thread(target=self.get_followers, args=(count, _qfr))
        _tfr.start(), _tfg.start()
        _tfr.join(), _tfg.join()
        return _qfg.get(), _qfr.get()

    def get_non_followers(self, count=1000) -> list[Any]:
        _followings, _followers = self._get_follow_data(1000000)
        return [each for each in _followings if each not in _followers][:count]

    def get_non_followings(self, count=1000) -> list[Any]:
        _followings, _followers = self._get_follow_data(1000000)
        return [each for each in _followers if each not in _followings][:count]


