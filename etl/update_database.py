import json

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

from common.repositories.mongo_data_store import MongoDataStore

from common.repositories.tag_repository import TagRepository

config = json.load(open("../etl/config.json"))
mongo_client = MongoClient()
transformer = SentenceTransformer(config["transformer_model"])
database_name = config["database_name"]
store = MongoDataStore(mongo_client, database_name, batch_size=100)
tag_repository = TagRepository(store)

recalculate_tag_embeddings(tag_repository, transformer)