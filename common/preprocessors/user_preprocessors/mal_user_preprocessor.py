from common.models.Platform import Platform
from common.models.user.media_entry import MediaEntry
from common.models.user.user import User
from common.preprocessors.user_preprocessors.user_preprocessor import UserPreprocessor
from common.repositories.media_repository import MediaRepository


class MalUserPreprocessor(UserPreprocessor):

    def __init__(self, anime_repository: MediaRepository, manga_repository: MediaRepository):
        self.anime_repository = anime_repository
        self.manga_repository = manga_repository
        self.anime_id_map = self._get_id_map(self.anime_repository)
        self.manga_id_map = self._get_id_map(self.manga_repository)

    def _get_id_map(self, repository):
        media_list = repository.get_multiple_media()
        return {media.id_mal: media.id for media in media_list if media.id_mal and media.id}

    def preprocess(self, raw_user_data):
        username = raw_user_data["User"]["username"]
        avatar_url = raw_user_data["User"]["avatar_url"]
        watched_anime = []
        read_manga = []
        planned_anime = []
        planned_manga = []

        for entry in raw_user_data["anime"]:
            mal_id = entry["mediaId"]
            watched_anime.append(MediaEntry(self.anime_id_map.get(mal_id), entry["score"]*10))

        for entry in raw_user_data["manga"]:
            mal_id = entry["mediaId"]
            read_manga.append(MediaEntry(self.manga_id_map.get(mal_id), entry["score"]*10))

        for entry in raw_user_data["planned_anime"]:
            mal_id = entry["mediaId"]
            planned_anime.append(self.anime_id_map.get(mal_id))

        for entry in raw_user_data["planned_manga"]:
            mal_id = entry["mediaId"]
            planned_manga.append(self.manga_id_map.get(mal_id))

        return User(username, Platform.MYANIMELIST, avatar_url, watched_anime, read_manga, planned_anime, planned_manga)
        
