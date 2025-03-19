

class UserFetchingService:
    def __init__(self, api: AnilistClient, user_preprocessor: UserPreprocessor):
        self.api = api
        self.user_preprocessor = user_preprocessor
        self.user_dictionary = {} # Probably a bad idea

    def fetch_user_data(self, username: str):
        if self.user_dictionary.get(username, None):
            return self.user_dictionary[username]

        raw_user_data = self.api.get_user_data(username)
        user = self.user_preprocessor.preprocess(raw_user_data)
        self.user_dictionary[username] = user
        
        return user
