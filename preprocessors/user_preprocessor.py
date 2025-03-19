

class UserPreprocessor():

    def preprocess(self, raw_user_data):
        avatar_url = raw_user_data["User"]["avatar"]["medium"]
        watched_anime = []
        read_manga = []
        planned_anime = []
        planned_manga = []

        for list_data in raw_user_data["anime"]["lists"]:
            for entry in list_data["entries"]:
                watched_anime.append(MediaEntry(entry["mediaId"], entry["score"]))

        for list_data in raw_user_data["manga"]["lists"]:
            for entry in list_data["entries"]:
                read_manga.append(MediaEntry(entry["mediaId"], entry["score"]))

        for list_data in raw_user_data["planned_anime"]["lists"]:
            for entry in list_data["entries"]:
                planned_anime.append(entry["mediaId"])

        for list_data in raw_user_data["planned_manga"]["lists"]:
            for entry in list_data["entries"]:
                planned_manga.append(entry["mediaId"])

        return User(avatar_url, watched_anime, read_manga, planned_anime, planned_manga)

    