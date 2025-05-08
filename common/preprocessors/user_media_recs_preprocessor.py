from common.models.user_media_recommendations import UserMediaRecommendations


class UserMediaRecsPreprocessor:

    def preprocess(self,
                   raw_media_list: list[dict]):
        recs_list = []

        for raw_media_data in raw_media_list:
            raw_recs_list = raw_media_data["recommendations"]["edges"]

            recommendations_dict = {}

            for recommendation in raw_recs_list:
                rec_node = recommendation["node"]

                media_recommendation = rec_node["mediaRecommendation"]

                if not media_recommendation:
                    continue

                rec_id = media_recommendation["id"]
                rec_rating = recommendation["node"]["rating"]

                recommendations_dict[rec_id] = rec_rating

            recs_list.append(UserMediaRecommendations(raw_media_data["id"], recommendations_dict))

        return recs_list