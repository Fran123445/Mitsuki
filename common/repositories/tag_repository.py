from typing import Any
from common.models.tag import Tag
from common.repositories.data_store import DataStore


class TagRepository:
    def __init__(self, store: DataStore, table: str = "tags"):
        self._store = store
        self._table = table

    def create_tag(self, tag: Tag) -> Any:
        return self._store.insert_one(self._table, tag)

    def create_many_tags(self, tag_list: list[Tag]) -> Any:
        return self._store.insert_many(self._table, tag_list)

    def get_tag_by_id(self, tag_id: int) -> Tag | None:
        return self._store.find_one(self._table, Tag, "tag_id", tag_id)

    def get_tag_by_name(self, tag_name: str) -> Tag | None:
        return self._store.find_one(self._table, Tag, "tag_name", tag_name)

    def get_all_tags(self) -> list[Tag]:
        return self._store.find_many(self._table, Tag)

    def update_tag(self, tag: Tag):
        return self._store.update_one(self._table, "tag_id", tag.id, tag)

    def get_total_amount(self) -> int:
        return self._store.count(self._table)