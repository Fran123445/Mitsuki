from common.repositories.repository import Repository
from common.models.user_media_recommendations import UserMediaRecommendations


class UserMediaRecommendationsRepository(Repository):

    def create_user_media_recommendation(self, user_media_recommendation: UserMediaRecommendations):
        return self.create(user_media_recommendation)

    def create_many_user_media_recommendations(self, user_media_recommendations: list[UserMediaRecommendations]):
        return self.create_many(user_media_recommendations)

    def get_user_media_recommendation_by_id(self, id: int):
        return self.get({"id": id}, UserMediaRecommendations)