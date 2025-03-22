from external_apis.anilist_api import AnilistApi
from external_apis.external_api import ExternalApi
from preprocessors.user_preprocessor import UserPreprocessor

class UserFetchingService:
    def __init__(self, api: ExternalApi, user_preprocessor: UserPreprocessor):
        self.api = api
        self.user_preprocessor = user_preprocessor
        self.user_dictionary = {} # Probably a bad idea

    def fetch_user_data(self, username: str):
        user = self.user_dictionary.get(username, None)

        if not user:
            raw_user_data = self.api.get_user_data(username)
            user = self.user_preprocessor.preprocess(raw_user_data)
            self.user_dictionary[username] = user
        
        return user

    def fetch_user_avatar(self, username: str):
        user = self.fetch_user_data(username)

        return {"username": user.username, "avatar_url": user.avatar_url}
