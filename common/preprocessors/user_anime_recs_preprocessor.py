from common.models.user_anime_recommendations import UserAnimeRecommendations


class UserAnimeRecsPreprocessor:

    def preprocess(self,
                   raw_anime_data):
        recommendation_list = raw_anime_data["recommendations"]["edge"]

        recommendations_dict = {}

        for recommendation in recommendation_list:
            rec_id = recommendation["node"]["mediaRecommendation"]["id"]
            rec_rating = recommendation["rating"]

            recommendations_dict[rec_id] = rec_rating

        return UserAnimeRecommendations(raw_anime_data["id"], recommendations_dict)