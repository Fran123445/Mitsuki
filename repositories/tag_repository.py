from pymongo import MongoClient
from models.tag import Tag
from repositories.repository import Repository


class TagRepository(Repository):
    def __init__(self, mongo_client: MongoClient, database_name: str = "tags"):
        super().__init__(mongo_client, database_name, 'tags')

    def create_tag(self, tag: Tag):
        return self.create(tag)

    def create_many_tags(self, tag_list: list[Tag]):
        return self.create_many(tag_list)

    def get_tag_by_id(self, tag_id: int):
        return self.get({"tag_id": tag_id}, Tag)

    def get_tag_by_index(self, tag_index: int):
        return self.get({"tag_index": tag_index}, Tag)
