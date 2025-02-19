import json
import time

import sentence_transformers
from pymongo import MongoClient

from api import AnilistClient
from recommendation import RecommendationEngine
from repositories.genre_repository import GenreRepository
from repositories.media_repository import MediaRepository
from repositories.tag_repository import TagRepository

from preprocessors.genre_preprocessor import GenrePreprocessor
from preprocessors.media_preprocessor import MediaPreprocessor
from preprocessors.tag_preprocessor import TagPreprocessor


def fill_database():
    if tag_repository.get_total_amount() == 0:
        tags = api_client.get_tags()
        tag_list = tag_preprocessor.preprocess(tags)
        tag_repository.create_many_tags(tag_list)

    if genre_repository.get_total_amount() == 0:
        genres = api_client.get_genres()
        genre_list = genre_preprocessor.preprocess(genres)
        genre_repository.create_many_genre(genre_list)

    if anime_repository.get_total_amount() == 0:
        for page in range(1, 201):
            anime_page = api_client.get_anime(page=page)
            anime_list = media_preprocessor.preprocess(anime_page)
            anime_repository.create_many_media(anime_list)
            time.sleep(2)  # avoid rate limit


def get_recommendations_from_user(username: str):
    user_anime_list = api_client.get_user_completed_list(username)
    user_anime_list = [anime for anime in user_anime_list if anime["score"] != 0]
    tag_profile, genre_profile = recommender.compute_user_profiles(user_anime_list)
    watched_anime_list = set([anime["media"]["id"] for anime in user_anime_list])

    return tag_profile, genre_profile, watched_anime_list


def get_recommendations_from_anime(anime_id: int):
    anime = anime_repository.get_media_by_id(anime_id)
    tag_profile = anime.media_embedding
    genre_profile = anime.media_genres

    return tag_profile, genre_profile


if __name__ == '__main__':
    config = json.load(open("config.json"))

    api_client = AnilistClient()

    transformer = sentence_transformers.SentenceTransformer(config["transformer_model"])

    mongo_client = MongoClient()
    database_name = config["database_name"]
    tag_repository = TagRepository(mongo_client, database_name)
    genre_repository = GenreRepository(mongo_client, database_name)
    anime_repository = MediaRepository(mongo_client, database_name, "anime")

    tag_preprocessor = TagPreprocessor(transformer)
    genre_preprocessor = GenrePreprocessor()
    media_preprocessor = MediaPreprocessor(genre_repository, tag_repository, transformer)

    fill_database()

    recommender = RecommendationEngine(anime_repository, tag_repository)

    user_input = input("Input username or anime ID: ")

    # a bit rough, but it's not like this part will be actually used
    while user_input:
        if user_input.isdigit():
            first_index = 1  # the first rec would match to the anime itself and that'd be stupid
            tag_profile, genre_profile = get_recommendations_from_anime(int(user_input))
            watched_anime_list = None
        else:
            first_index = 0
            tag_profile, genre_profile, watched_anime_list = get_recommendations_from_user(user_input)

        recs = recommender.get_recommendations(tag_profile, genre_profile, watched_anime_list, weight_genres=0.33,
                                               top_n=17)

        for idx, anime in enumerate(recs[first_index:]):
            print(f"{idx + 1} - {anime[0]}: {anime[1]:.5f}")

        user_input = input("\nInput username or anime ID: ")
