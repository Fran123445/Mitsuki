import json
import os
import sentence_transformers
from dotenv import load_dotenv
from pymongo import MongoClient

from common.external_apis.anilist_api import AnilistApi
from common.preprocessors.genre_preprocessor import GenrePreprocessor
from common.preprocessors.media_preprocessor import MediaPreprocessor
from common.preprocessors.tag_preprocessor import TagPreprocessor
from common.preprocessors.user_media_recs_preprocessor import UserMediaRecsPreprocessor
from common.repositories.genre_repository import GenreRepository
from common.repositories.media_repository import MediaRepository
from common.repositories.tag_repository import TagRepository
from common.repositories.user_anime_recs_repository import UserMediaRecommendationsRepository

def main():
    load_dotenv()
    
    # --- Configuration & Clients ---
    config = json.load(open("etl/config.json"))
    db_name = config["database_name"]
    batch_size = int(os.getenv("MONGO_BATCH_SIZE", 100))
    
    api_client = AnilistApi()
    mongo_client = MongoClient()
    transformer = sentence_transformers.SentenceTransformer(config["transformer_model"])

    # --- Repositories ---
    repos = {
        "tag": TagRepository(mongo_client, db_name, batch_size, "tags"),
        "genre": GenreRepository(mongo_client, db_name, batch_size, "genres"),
        "anime": MediaRepository(mongo_client, db_name, batch_size, "anime"),
        "manga": MediaRepository(mongo_client, db_name, batch_size, "manga"),
        "user_anime_recs": UserMediaRecommendationsRepository(mongo_client, db_name, batch_size, "user_anime_recommendations"),
        "user_manga_recs": UserMediaRecommendationsRepository(mongo_client, db_name, batch_size, "user_manga_recommendations")
    }

    # --- Preprocessors ---
    pre = {
        "tag": TagPreprocessor(transformer),
        "genre": GenrePreprocessor(transformer),
        "media": MediaPreprocessor(repos["genre"], repos["tag"], transformer),
        "user_recs": UserMediaRecsPreprocessor()
    }

    # --- Execution ---
    fill_tags(api_client, repos["tag"], pre["tag"])
    fill_genres(api_client, repos["genre"], pre["genre"])
    
    fill_media_type(api_client, "anime", repos["anime"], repos["user_anime_recs"], pre["media"], pre["user_recs"])
    fill_media_type(api_client, "manga", repos["manga"], repos["user_manga_recs"], pre["media"], pre["user_recs"])

def fill_tags(api, repo, preprocessor):
    if repo.get_total_amount() == 0:
        print("Processing Tags...")
        data = api.get_tags()
        tags = preprocessor.preprocess(data)
        repo.create_many_tags(tags)
        print("Tags loaded")

def fill_genres(api, repo, preprocessor):
    if repo.get_total_amount() == 0:
        print("Processing Genres...")
        data = api.get_genres()
        genres = preprocessor.preprocess(data)
        repo.create_many_genre(genres)
        print("Genres loaded")

def fill_media_type(api, media_type, media_repo, recs_repo, media_pre, recs_pre):
    """Generic function to load anime or manga data."""
    if media_repo.get_total_amount() == 0:
        print(f"Processing {media_type.capitalize()}...")
        get_method = getattr(api, f"get_{media_type}")
        
        for page in range(1, 201):
            print(f"{media_type.capitalize()} Page: {page}")
            page_data = get_method(page=page, recs_per_page=100)
            
            media_list = media_pre.preprocess(page_data)
            recs_list = recs_pre.preprocess(page_data)

            media_repo.create_many_media(media_list)
            recs_repo.create_many_user_media_recommendations(recs_list)
            
        print(f"{media_type.capitalize()} loaded")

if __name__ == "__main__":
    main()
