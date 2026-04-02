from common.models.tag import Tag
from common.repositories.data_store import DataStore


class TagRepository:
    def __init__(self, store: DataStore, collection: str = "tags"):
        self._store = store
        self._collection = collection

    def create_tag(self, tag: Tag):
        return self._store.insert_one(self._collection, tag.to_dict())

    def create_many_tags(self, tag_list: list[Tag]):
        return self._store.insert_many(self._collection, [t.to_dict() for t in tag_list])

    def get_tag_by_id(self, tag_id: int) -> Tag | None:
        doc = self._store.find_one(self._collection, {"tag_id": tag_id})
        return Tag.from_dict(doc) if doc else None

    def get_tag_by_name(self, tag_name: str) -> Tag | None:
        doc = self._store.find_one(self._collection, {"tag_name": tag_name})
        return Tag.from_dict(doc) if doc else None

    def get_all_tags(self) -> list[Tag]:
        docs = self._store.find_many(self._collection, {})
        return [Tag.from_dict(d) for d in docs]

    def update_tag(self, tag: Tag):
        return self._store.update_one(self._collection, {"tag_id": tag.id}, tag.to_dict())

    def get_total_amount(self) -> int:
        return self._store.count(self._collection)