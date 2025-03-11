import numpy as np

from repositories.genre_repository import GenreRepository
from services.recommendation_service.media_list_filters.media_list_filter import MediaListFilter


class GenreExclusionFilter(MediaListFilter):

    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    def filter(self, media_list: list, params: dict):
        super()

        excluded_genres = params.get("excluded_genres")
        excluded_genres_indices = self.get_genre_indices(excluded_genres)

        filtered_anime = [
            media for media in media_list
            if not np.any(media.genres[excluded_genres_indices] == 1)
        ]

        return filtered_anime

    def check_valid_params(self, params: dict):
        return bool(params.get("excluded_genres")) # empty list is cast to false, otherwise true

    def get_genre_indices(self, excluded_genres: list):
        return [self.genre_repository.get_genre_by_name(genre).index for genre in excluded_genres]