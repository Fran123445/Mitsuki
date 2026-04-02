from common.models.media import Media
from common.repositories.data_store import DataStore


class MediaRepository:
    def __init__(self, store: DataStore, collection: str = "anime"):
        self._store = store
        self._collection = collection
        self._cache = None

    def create_media(self, media: Media):
        return self._store.insert_one(self._collection, media.to_dict())

    def create_many_media(self, media_list: list[Media]):
        return self._store.insert_many(self._collection, [m.to_dict() for m in media_list])

    def get_media_by_id(self, media_id: int) -> Media | None:
        if not self._cache:
            self._create_cache()
        return self._cache.get(media_id)

    def get_all_media(self) -> list[Media]:
        if not self._cache:
            self._create_cache()
        return list(self._cache.values())

    def get_total_amount(self) -> int:
        return self._store.count(self._collection)

    def _create_cache(self):
        docs = self._store.find_many(self._collection, {})
        media_list = [Media.from_dict(d) for d in docs]
        self._cache = {media.id: media for media in media_list}
