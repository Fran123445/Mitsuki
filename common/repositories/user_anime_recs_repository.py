from common.repositories.data_store import DataStore
from common.models.user_media_recommendations import UserMediaRecommendations


class UserMediaRecommendationsRepository:
    def __init__(self, store: DataStore, collection: str = "user_anime_recommendations"):
        self._store = store
        self._collection = collection
        self._cache = {}

    def create_user_media_recommendation(self, user_media_recommendation: UserMediaRecommendations):
        return self._store.insert_one(self._collection, user_media_recommendation.to_dict())

    def create_many_user_media_recommendations(self, user_media_recommendations: list[UserMediaRecommendations]):
        return self._store.insert_many(self._collection, [r.to_dict() for r in user_media_recommendations])

    def get_user_media_recommendation_by_id(self, id: int) -> UserMediaRecommendations | None:
        if not self._cache:
            docs = self._store.find_many(self._collection, {})
            recs = [UserMediaRecommendations.from_dict(d) for d in docs]
            self._cache = {rec.id: rec for rec in recs}

        if id in self._cache:
            return self._cache[id]

        doc = self._store.find_one(self._collection, {"id": id})
        return UserMediaRecommendations.from_dict(doc) if doc else None

    def get_total_amount(self) -> int:
        return self._store.count(self._collection)