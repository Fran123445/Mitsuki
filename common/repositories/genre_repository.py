from typing import Any
from common.models.genre import Genre
from common.repositories.data_store import DataStore


class GenreRepository:
    def __init__(self, store: DataStore, table: str = "genres"):
        self._store = store
        self._table = table

    def create_genre(self, genre: Genre) -> Any:
        return self._store.insert_one(self._table, genre)

    def create_many_genre(self, genre_list: list[Genre]) -> Any:
        return self._store.insert_many(self._table, genre_list)

    def get_genre_by_name(self, genre_name: str) -> Genre | None:
        return self._store.find_one(self._table, Genre, "genre_name", genre_name)

    def get_all_genres(self) -> list[Genre]:
        return self._store.find_many(self._table, Genre)

    def get_total_amount(self) -> int:
        return self._store.count(self._table)