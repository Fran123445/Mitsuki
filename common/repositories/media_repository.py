from typing import Any
from common.models.media import Media
from common.repositories.data_store import DataStore


class MediaRepository:
    def __init__(self, store: DataStore, table: str = "anime"):
        self._store = store
        self._table = table
        self._cache = None

    def create_media(self, media: Media) -> Any:
        return self._store.insert_one(self._table, media)

    def create_many_media(self, media_list: list[Media]) -> Any:
        return self._store.insert_many(self._table, media_list)

    def get_media_by_id(self, media_id: int) -> Media | None:
        if not self._cache:
            self._create_cache()
        return self._cache.get(media_id)

    def get_all_media(self) -> list[Media]:
        if not self._cache:
            self._create_cache()
        return list(self._cache.values())

    def get_total_amount(self) -> int:
        return self._store.count(self._table)

    def _create_cache(self):
        media_list = self._store.find_many(self._table, Media)
        self._cache = {media.id: media for media in media_list}
