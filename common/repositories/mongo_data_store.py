from typing import Any, TypeVar
from pymongo import MongoClient

T = TypeVar("T")


class MongoDataStore:
    def __init__(self, mongo_client: MongoClient, database_name: str, batch_size: int):
        self._db = mongo_client[database_name]
        self._batch_size = batch_size

    def insert_one(self, table: str, object: T) -> Any:
        result = self._db[table].insert_one(object.to_dict())
        return result.inserted_id

    def insert_many(self, table: str, objects: list[T]) -> Any:
        result = self._db[table].insert_many([obj.to_dict() for obj in objects])
        return result.inserted_ids

    def find_one(self, table: str, model_class: type[T], field: str, value: Any) -> T | None:
        doc = self._db[table].find_one({field: value})
        return model_class.from_dict(doc) if doc else None

    def find_many(
        self,
        table: str,
        model_class: type[T],
        field: str | None = None,
        value: Any | None = None,
    ) -> list[T]:
        query = {field: value} if field else {}
        cursor = self._db[table].find(query).batch_size(self._batch_size)
        return [model_class.from_dict(doc) for doc in cursor]

    def count(self, table: str) -> int:
        return self._db[table].count_documents({})

    def update_one(self, table: str, field: str, value: Any, object: T) -> int:
        result = self._db[table].update_one({field: value}, {"$set": object.to_dict()})
        return result.modified_count
