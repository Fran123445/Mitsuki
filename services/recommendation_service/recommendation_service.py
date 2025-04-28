import numpy as np

from models.Platform import Platform
from models.user.user import User
from repositories.media_repository import MediaRepository
from services.recommendation_service.recommendation_engine import RecommendationEngine
from services.recommendation_service.user_rec_profile_processor import UserRecProfileProcessor


class RecommendationService:

    def __init__(self,
                 media_repository: MediaRepository,
                 user_rec_profile_processor: UserRecProfileProcessor,
                 recommendation_engine: RecommendationEngine,
                 filter_list: list,
                 weight_genres: float = 0.5):
        self.media_repository = media_repository
        self.recommendation_engine = recommendation_engine
        self.user_rec_profile_processor = user_rec_profile_processor
        self.filter_list = filter_list
        self.weight_genres = weight_genres

    def _create_return_list(self,
                            recommendation_list: list,
                            user: User = None):
        return_list = []

        for media_id, score in recommendation_list:
            media = self.media_repository.get_media_by_id(media_id)

            id = media.id if not (user and user.platform == Platform.MYANIMELIST) else media.id_mal

            return_list.append({
                "id": id,
                "title": media.title_romaji,
                "image_url": media.image_url,
                "score": score
            })

        return return_list

    def _get_recommendations(self,
                             excluded_media: list,
                             tag_profile: np.ndarray,
                             genre_profile: np.ndarray,
                             filter_params: dict = None):
        media_list = self.media_repository.get_multiple_media()

        excluded_ids_set = {entry.id for entry in excluded_media}

        media_list = [media for media in media_list if media.id not in excluded_ids_set]

        if not filter_params:
            filter_params = {}

        for filter_object in self.filter_list:
            media_list = filter_object.filter(media_list, filter_params)

        recommendation_dict = self.recommendation_engine.get_recommendations(media_list,
                                                                             tag_profile,
                                                                             genre_profile,
                                                                             weight_genres=self.weight_genres
                                                                             )

        return recommendation_dict

    def get_recommendations_from_media(self, media_id: int, top_n: int, filter_params: dict):
        media = self.media_repository.get_media_by_id(media_id)
        tag_profile = media.tag_embedding
        genre_profile = media.genre_embedding

        recommendations = self._get_recommendations([media], tag_profile, genre_profile, filter_params)

        return self._create_return_list(recommendations[:top_n])


    def get_recommendations_from_user(self, user: User, top_n: int, filter_params: dict):
        tag_profile, genre_profile = self.user_rec_profile_processor.compute_user_profiles(user)

        media_list = self.user_rec_profile_processor.get_media_list(user)

        recommendations = self._get_recommendations(media_list, tag_profile, genre_profile, filter_params)

        return self._create_return_list(recommendations[:top_n], user)

