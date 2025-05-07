from pymongo import MongoClient
from common.models.media import Media
from common.repositories.repository import Repository


class MediaRepository(Repository):
    def __init__(self,
                 mongo_client: MongoClient,
                 database_name: str,
                 batch_size: int,
                 collection_name: str = "anime"):
        super().__init__(mongo_client, database_name, batch_size, collection_name)
        self.cache = None

    def create_media(self, media: Media):
        return self.create(media)

    def create_many_media(self, media_list: list[Media]):
        return self.create_many(media_list)

    def get_media_by_id(self, media_id: int):
        if not self.cache:
            self.create_cache()

        return self.cache.get(media_id)

    def get_multiple_media(self, filter: dict = None, projection: dict = None):
        if filter is None and projection is None:
            if not self.cache:
                self.create_cache()
                
            return list(self.cache.values()) # not exactly performant but ram is limited

        return self.get_multiple(Media, filter, projection)

    def create_cache(self):
        media_list = self.get_multiple(Media)
        self.cache = {media.id: media for media in media_list}
