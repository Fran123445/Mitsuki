from pymongo import MongoClient
from models.media import Media
from repositories.repository import Repository


class MediaRepository(Repository):
    def __init__(self, mongo_client: MongoClient, database_name: str, collection_name: str = "anime"):
        super().__init__(mongo_client, database_name, collection_name)
        self.cache = None

    def create_media(self, media: Media):
        return self.create(media)

    def create_many_media(self, media_list: list[Media]):
        return self.create_many(media_list)

    def get_media_by_id(self, media_id: int):
        return self.get({"id": media_id}, Media)

    def get_multiple_media(self, filter: dict = None, projection: dict = None):
        if filter is None and projection is None:
            if not self.cache:
                self.cache = self.get_multiple(Media, filter, projection)
                
            return self.cache

        return self.get_multiple(Media, filter, projection)
