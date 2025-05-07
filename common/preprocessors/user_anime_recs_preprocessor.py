from common.models.user_anime_recommendations import UserAnimeRecommendations


class UserAnimeRecsPreprocessor:

    def preprocess(self,
                   raw_media_list: list[dict]):
        recs_list = []

        for raw_media_data in raw_media_list:
            raw_recs_list = raw_media_data["recommendations"]["edge"]

            recommendations_dict = {}

            for recommendation in raw_recs_list:
                rec_id = recommendation["node"]["mediaRecommendation"]["id"]
                rec_rating = recommendation["rating"]

                recommendations_dict[rec_id] = rec_rating

            recs_list.append(UserAnimeRecommendations(raw_media_data["id"], recommendations_dict))

        return recs_list