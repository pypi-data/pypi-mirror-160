from enum import unique, Enum

@unique
class Url(Enum):
    user = 'https://api.github.com/users/{}'
    repo = 'https://api.github.com/users/{}/repos?per_page={}'
    follower = 'https://api.github.com/users/{}/followers?per_page={}'
    following = 'https://api.github.com/users/{}/following?per_page={}'