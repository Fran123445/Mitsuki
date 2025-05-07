from common.repositories.repository import Repository
from ml_model.models.user_anime_recommendations import UserAnimeRecommendations


class UserAnimeRecommendationsRepository(Repository):

    def create_user_anime_recommendation(self, user_anime_recommendation: UserAnimeRecommendations):
        return self.create(user_anime_recommendation)

    def create_many_user_anime_recommendations(self, user_anime_recommendations: list[UserAnimeRecommendations]):
        return self.create_many(user_anime_recommendations)

    def get_user_anime_recommendation_by_anime_id(self, id: int):
        return self.get({"id": id}, UserAnimeRecommendations)