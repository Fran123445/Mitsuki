import json
import os
import time

import sentence_transformers
from dotenv import load_dotenv
from pymongo import MongoClient

from common.external_apis.anilist_api import AnilistApi
from common.preprocessors.genre_preprocessor import GenrePreprocessor
from common.preprocessors.media_preprocessor import MediaPreprocessor
from common.preprocessors.tag_preprocessor import TagPreprocessor
from common.repositories.genre_repository import GenreRepository
from common.repositories.media_repository import MediaRepository
from common.repositories.tag_repository import TagRepository

load_dotenv()

batch_size = int(os.getenv("MONGO_BATCH_SIZE"))

config = json.load(open("../etl/config.json"))

api_client = AnilistApi()

mongo_client = MongoClient()
database_name = config["database_name"]
tag_repository = TagRepository(mongo_client, batch_size, database_name)
genre_repository = GenreRepository(mongo_client, batch_size, database_name)
anime_repository = MediaRepository(mongo_client, database_name, batch_size, "anime")
manga_repository = MediaRepository(mongo_client, database_name, batch_size,"manga")

transformer = sentence_transformers.SentenceTransformer(config["transformer_model"])

tag_preprocessor = TagPreprocessor(transformer)
genre_preprocessor = GenrePreprocessor(transformer)
media_preprocessor = MediaPreprocessor(genre_repository, tag_repository, transformer)

if tag_repository.get_total_amount() == 0:
    tags = api_client.get_tags()
    tag_list = tag_preprocessor.preprocess(tags)
    tag_repository.create_many_tags(tag_list)

print("Tags loaded")

if genre_repository.get_total_amount() == 0:
    genres = api_client.get_genres()
    genre_list = genre_preprocessor.preprocess(genres)
    genre_repository.create_many_genre(genre_list)

print("Genres loaded")

if anime_repository.get_total_amount() == 0:
    for page in range(1, 201):
        print(page)
        anime_page = api_client.get_anime(page=page)
        anime_list = media_preprocessor.preprocess(anime_page)
        anime_repository.create_many_media(anime_list)
        time.sleep(2)  # avoid rate limit

print("Anime loaded")

if manga_repository.get_total_amount() == 0:
    for page in range(1, 201):
        print(page)
        manga_page = api_client.get_manga(page=page)
        manga_list = media_preprocessor.preprocess(manga_page)
        manga_repository.create_many_media(manga_list)
        time.sleep(2)  # avoid rate limit

print("Manga loaded")