from models.user.media_entry import MediaEntry
from models.user.user import User
from preprocessors.user_preprocessors.user_preprocessor import UserPreprocessor

class MalUserPreprocessor(UserPreprocessor):
    
    def preprocess(self, raw_user_data):
        username = raw_user_data["User"]["username"]
        avatar_url = raw_user_data["User"]["avatar_url"]
        watched_anime = []
        read_manga = []
        planned_anime = []
        planned_manga = []

        for entry in raw_user_data["anime"]:
            watched_anime.append(MediaEntry(entry["mediaId"], entry["score"]))

        for entry in raw_user_data["manga"]:
            read_manga.append(MediaEntry(entry["mediaId"], entry["score"]))

        for entry in raw_user_data["planned_anime"]:
            planned_anime.append(entry["mediaId"])

        for entry in raw_user_data["planned_manga"]:
            planned_manga.append(entry["mediaId"])

        return User(username, avatar_url, watched_anime, read_manga, planned_anime, planned_manga)
        
