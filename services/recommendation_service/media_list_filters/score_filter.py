from services.recommendation_service.media_list_filters.media_list_filter import MediaListFilter


class ScoreFilter(MediaListFilter):

    def filter(self, media_list: list, params: dict):
        super()

        minimum_score = params.get("minimum_score", 0)
        maximum_score = params.get("maximum_score", 100)

        return [media for media in media_list if minimum_score <= media.mean_score <= maximum_score]