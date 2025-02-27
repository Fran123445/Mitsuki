from datetime import datetime

from services.recommendation_service.media_list_filters.media_list_filter import MediaListFilter


class YearFilter(MediaListFilter):

    def filter(self, media_list: list, params: dict):
        initial_year = params.get("initial_year", 1900)
        final_year = params.get("final_year", datetime.now().year)

        return [media for media in media_list if initial_year <= media.year <= final_year]