from pymongo import MongoClient
import numpy as np

class DatabaseClient:
    def __init__(self, db_name="AnilistData"):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.tags_collection = self.db["tags"]
        self.genres_collection = self.db["genres"]
        self.anime_collection = self.db["anime"]

    def insert_tags(self, tags: list):
        for idx, tag in enumerate(tags):
            tag["index"] = idx
            self.tags_collection.insert_one(tag)

    def insert_genres(self, genres: list):
        for idx, genre in enumerate(genres):
            self.genres_collection.insert_one({"name": genre, "index": idx})

    def insert_anime(self, anime_data: list):
        tags_size = self.tags_collection.count_documents({})
        genres_size = self.genres_collection.count_documents({})

        for anime in anime_data:
            # Create feature vectors
            tag_ranks = np.zeros(tags_size)
            genre_features = np.zeros(genres_size)

            # Process tags
            for tag in anime.get('tags', []):
                tag_doc = self.tags_collection.find_one({'id': tag['id']})
                tag_ranks[tag_doc['index']] = tag.get('rank', 0)

            # Process genres
            for genre in anime.get('genres', []):
                genre_doc = self.genres_collection.find_one({'name': genre})
                genre_features[genre_doc['index']] = 1

            anime_record = {
                'id': anime['id'],
                'title': anime['title']['romaji'],
                'tags': tag_ranks,
                'genres': genre_features,
                'description': anime.get('description', '')
            }

            self.anime_collection.insert_one(anime_record)

    def get_anime_by_id(self, anime_id):
        return self.anime_collection.find_one({"id": anime_id})