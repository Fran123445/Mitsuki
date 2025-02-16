from pymongo import MongoClient
from models.media import Media
from repositories.repository import Repository


class MediaRepository(Repository):
    def __init__(self, mongo_client: MongoClient, database_name: str, collection_name: str = "anime"):
        super().__init__(mongo_client, database_name, collection_name)

    def create_media(self, media: Media):
        return self.create(media)

    def get_media_by_id(self, media_id: int):
        return self.get({"media_id": media_id}, Media)
