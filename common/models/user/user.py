from common.models.Platform import Platform
from common.models.user.media_entry import MediaEntry

class User:

    def __init__(self, username: str,
                 platform: Platform,
                 avatar_url: str,
                 watched_anime: list[MediaEntry],
                 read_manga: list[MediaEntry],
                 planned_anime: list[int],
                 planned_manga: list[int]):
        self.username = username
        self.platform = platform
        self.avatar_url = avatar_url
        self.watched_anime = watched_anime
        self.read_manga = read_manga
        self.planned_anime = planned_anime
        self.planned_manga = planned_manga