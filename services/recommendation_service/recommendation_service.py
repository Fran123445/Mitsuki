from repositories.media_repository import MediaRepository
from services.recommendation_service.recommendation_engine import RecommendationEngine


class RecommendationService:

    def __init__(self,
                 media_repository: MediaRepository,
                 recommendation_engine: RecommendationEngine,
                 weight_genres: float = 0.5):
        self.media_repository = media_repository
        self.weight_genres = weight_genres
        self.recommendation_engine = recommendation_engine

    def _create_return_list(self, recommendation_list: list):
        return_list = []

        for media_id, score in recommendation_list:
            media = self.media_repository.get_media_by_id(media_id)
            return_list.append({
                "title": media.media_title_romaji,
                "image_url": media.image_url,
                "score": score
            })

        return return_list

    def get_recommendations_from_media(self, media_id: int, top_n: int = 10):
        media = self.media_repository.get_media_by_id(media_id)
        tag_profile = media.media_embedding
        genre_profile = media.media_genres

        recommendation_dict = self.recommendation_engine.get_recommendations(tag_profile,
                                                                             genre_profile,
                                                                             weight_genres=self.weight_genres
                                                                             )

        return self._create_return_list(recommendation_dict[1:top_n+1])
