from common.models.genre import Genre
from common.repositories.data_store import DataStore


class GenreRepository:
    def __init__(self, store: DataStore, collection: str = "genres"):
        self._store = store
        self._collection = collection

    def create_genre(self, genre: Genre):
        return self._store.insert_one(self._collection, genre.to_dict())

    def create_many_genre(self, genre_list: list[Genre]):
        return self._store.insert_many(self._collection, [g.to_dict() for g in genre_list])

    def get_genre_by_name(self, genre_name: str) -> Genre | None:
        doc = self._store.find_one(self._collection, {"genre_name": genre_name})
        return Genre.from_dict(doc) if doc else None

    def get_all_genres(self) -> list[Genre]:
        docs = self._store.find_many(self._collection, {})
        return [Genre.from_dict(d) for d in docs]

    def get_total_amount(self) -> int:
        return self._store.count(self._collection)