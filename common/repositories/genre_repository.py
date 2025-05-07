from common.models.genre import Genre
from common.repositories.repository import Repository


class GenreRepository(Repository):
    def create_genre(self, genre: Genre):
        return self.create(genre)

    def create_many_genre(self, genre_list: list[Genre]):
        return self.create_many(genre_list)

    def get_genre_by_name(self, genre_name: str):
        return self.get({"genre_name": genre_name}, Genre)
