from pymongo import MongoClient


class MongoDataStore:
    def __init__(self, mongo_client: MongoClient, database_name: str, batch_size: int):
        self._db = mongo_client[database_name]
        self._batch_size = batch_size

    def insert_one(self, collection: str, document: dict):
        return self._db[collection].insert_one(document)

    def insert_many(self, collection: str, documents: list[dict]):
        return self._db[collection].insert_many(documents)

    def find_one(self, collection: str, query: dict) -> dict | None:
        return self._db[collection].find_one(query)

    def find_many(self, collection: str, query: dict, projection: dict | None = None) -> list[dict]:
        cursor = self._db[collection].find(query or {}, projection).batch_size(self._batch_size)
        return list(cursor)

    def count(self, collection: str) -> int:
        return self._db[collection].count_documents({})

    def update_one(self, collection: str, query: dict, document: dict) -> int:
        result = self._db[collection].update_one(query, {"$set": document})
        return result.modified_count
