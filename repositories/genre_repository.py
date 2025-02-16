from pymongo import MongoClient
from models.genre import Genre
from repositories.repository import Repository


class GenreRepository(Repository):
    def __init__(self, mongo_client: MongoClient, database_name: str = "genres"):
        super().__init__(mongo_client, database_name, 'genres')

    def create_genre(self, genre: Genre):
        return self.create(genre)

    def get_genre_by_name(self, genre_name: str):
        return self.get({"genre_name": genre_name}, Genre)
