from pymongo import MongoClient
from common.models.tag import Tag
from common.repositories.repository import Repository


class TagRepository(Repository):
    def __init__(self,
                 mongo_client: MongoClient,
                 batch_size: int,
                 database_name: str = "tags"):
        super().__init__(mongo_client, database_name, 'tags', batch_size)

    def create_tag(self, tag: Tag):
        return self.create(tag)

    def create_many_tags(self, tag_list: list[Tag]):
        return self.create_many(tag_list)

    def get_tag_by_id(self, tag_id: int):
        return self.get({"tag_id": tag_id}, Tag)

    def get_tag_by_name(self, tag_name: str):
        return self.get({"tag_name": tag_name}, Tag)

    def get_multiple_tags(self, filter: dict = None, projection: dict = None):
        return self.get_multiple(Tag, filter, projection)

    def update_tag(self, tag: Tag):
        return self.update({"tag_id": tag.id}, tag)