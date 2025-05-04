from web_service.services.recommendation_service.media_list_filters.media_list_filter import MediaListFilter


class GenreFilter(MediaListFilter):

    def __init__(self, exclude: bool):
        self.param_key = "excluded_genres" if exclude else "included_genres"
        self.exclude = exclude

    def filter(self, media_list: list, params: dict):
        super()

        genres = params.get(self.param_key)

        if self.exclude:
            filtered_anime = [
                media for media in media_list
                if all(genre not in media.genres for genre in genres)
            ]
        else:
            filtered_anime = [
                media for media in media_list
                if all(genre in media.genres for genre in genres)
            ]

        return filtered_anime

    def check_valid_params(self, params: dict):
        return bool(params.get(self.param_key)) # empty list is cast to false, otherwise true