import numpy as np

from repositories.genre_repository import GenreRepository
from services.recommendation_service.media_list_filters.media_list_filter import MediaListFilter


class GenreFilter(MediaListFilter):

    def __init__(self, genre_repository: GenreRepository, exclude: bool):
        self.genre_repository = genre_repository
        self.exclusion_value = 1 if exclude else 0
        self.param_key = "excluded_genres" if exclude else "included_genres"

    def filter(self, media_list: list, params: dict):
        super()

        genres = params.get(self.param_key)
        genres_indices = self.get_genre_indices(genres)

        filtered_anime = [
            media for media in media_list
            if not np.any(media.genres[genres_indices] == self.exclusion_value)
        ]

        return filtered_anime

    def check_valid_params(self, params: dict):
        return bool(params.get(self.param_key)) # empty list is cast to false, otherwise true

    def get_genre_indices(self, genres: list):
        return [self.genre_repository.get_genre_by_name(genre).index for genre in genres]