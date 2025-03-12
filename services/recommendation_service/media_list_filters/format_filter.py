from services.recommendation_service.media_list_filters.media_list_filter import MediaListFilter


class FormatFilter(MediaListFilter):

    def filter(self, media_list: list, params: dict):
        super()

        formats = set(params.get("formats"))

        return [media for media in media_list if media.format in formats]

    def check_valid_params(self, params: dict):
        return not bool(params.get("formats"))