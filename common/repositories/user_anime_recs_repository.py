from typing import Any
from common.repositories.data_store import DataStore
from common.models.user_media_recommendations import UserMediaRecommendations


class UserMediaRecommendationsRepository:
    def __init__(self, store: DataStore, table: str = "user_anime_recommendations"):
        self._store = store
        self._table = table
        self._cache = {}

    def create_user_media_recommendation(self, user_media_recommendation: UserMediaRecommendations) -> Any:
        return self._store.insert_one(self._table, user_media_recommendation)

    def create_many_user_media_recommendations(self, user_media_recommendations: list[UserMediaRecommendations]) -> Any:
        return self._store.insert_many(self._table, user_media_recommendations)

    def get_user_media_recommendation_by_id(self, id: int) -> UserMediaRecommendations | None:
        if not self._cache:
            recs = self._store.find_many(self._table, UserMediaRecommendations)
            self._cache = {rec.id: rec for rec in recs}

        if id in self._cache:
            return self._cache[id]

        return self._store.find_one(self._table, UserMediaRecommendations, "id", id)

    def get_total_amount(self) -> int:
        return self._store.count(self._table)