import json
import os
import sentence_transformers
from typing import List, Tuple
from dotenv import load_dotenv
from pymongo import MongoClient

from common.repositories.mongo_data_store import MongoDataStore
from common.external_apis.anilist_api import AnilistApi
from common.preprocessors.genre_preprocessor import GenrePreprocessor
from common.preprocessors.media_preprocessor import MediaPreprocessor
from common.preprocessors.tag_preprocessor import TagPreprocessor
from common.preprocessors.user_media_recs_preprocessor import UserMediaRecsPreprocessor
from common.repositories.genre_repository import GenreRepository
from common.repositories.media_repository import MediaRepository
from common.repositories.tag_repository import TagRepository
from common.repositories.user_anime_recs_repository import UserMediaRecommendationsRepository

# ETL Configuration
BATCH_SIZE = 100
MAX_PAGES = 200

# --- Extraction Layer ---
def extract_tags(api: AnilistApi) -> List:
    return api.get_tags()

def extract_genres(api: AnilistApi) -> List:
    return api.get_genres()

def extract_media_page(api: AnilistApi, media_type: str, page: int) -> List:
    get_method = getattr(api, f"get_{media_type}")
    return get_method(page=page, recs_per_page=BATCH_SIZE)

# --- Transformation Layer ---
def transform_tags(preprocessor: TagPreprocessor, raw_tags: List):
    return preprocessor.preprocess(raw_tags)

def transform_genres(preprocessor: GenrePreprocessor, raw_genres: List):
    return preprocessor.preprocess(raw_genres)

def transform_media(media_pre: MediaPreprocessor, recs_pre: UserMediaRecsPreprocessor, raw_media: List) -> Tuple[List, List]:
    media_list = media_pre.preprocess(raw_media)
    recs_list = recs_pre.preprocess(raw_media)
    return media_list, recs_list

# --- Loading Layer ---
def load_tags(repo: TagRepository, tags: List):
    repo.create_many_tags(tags)

def load_genres(repo: GenreRepository, genres: List):
    repo.create_many_genre(genres)

def load_media(media_repo: MediaRepository, recs_repo: UserMediaRecommendationsRepository, media_list: List, recs_list: List):
    media_repo.create_many_media(media_list)
    recs_repo.create_many_user_media_recommendations(recs_list)

# --- Job Orchestration ---
def etl_tags_job(api: AnilistApi, repo: TagRepository, pre: TagPreprocessor):
    if repo.get_total_amount() > 0:
        print("[Job: Tags] Already populated. Skipping.")
        return

    print("[Job: Tags] Starting Extraction...")
    raw = extract_tags(api)
    
    print("[Job: Tags] Starting Transformation...")
    transformed = transform_tags(pre, raw)
    
    print("[Job: Tags] Starting Loading...")
    load_tags(repo, transformed)
    print("[Job: Tags] Completed.")

def etl_genres_job(api: AnilistApi, repo: GenreRepository, pre: GenrePreprocessor):
    if repo.get_total_amount() > 0:
        print("[Job: Genres] Already populated. Skipping.")
        return

    print("[Job: Genres] Starting Extraction...")
    raw = extract_genres(api)
    
    print("[Job: Genres] Starting Transformation...")
    transformed = transform_genres(pre, raw)
    
    print("[Job: Genres] Starting Loading...")
    load_genres(repo, transformed)
    print("[Job: Genres] Completed.")

def etl_media_job(api: AnilistApi, media_type: str, media_repo: MediaRepository, recs_repo: UserMediaRecommendationsRepository, media_pre: MediaPreprocessor, recs_pre: UserMediaRecsPreprocessor):
    if media_repo.get_total_amount() > 0:
        print(f"[Job: {media_type.capitalize()}] Already populated. Skipping.")
        return

    print(f"[Job: {media_type.capitalize()}] Starting Pipeline...")
    for page in range(1, MAX_PAGES + 1):
        print(f"  > Processing {media_type.capitalize()} Page {page}/{MAX_PAGES}...")
        
        # E, T, L in sequence for each page
        raw = extract_media_page(api, media_type, page)
        media_list, recs_list = transform_media(media_pre, recs_pre, raw)
        load_media(media_repo, recs_repo, media_list, recs_list)
        
    print(f"[Job: {media_type.capitalize()}] Completed.")

def main():
    load_dotenv()
    
    # Initialization
    with open("etl/config.json", "r") as f:
        config = json.load(f)
    
    db_name = config["database_name"]
    batch_size = int(os.getenv("MONGO_BATCH_SIZE", BATCH_SIZE))
    
    # Clients
    api_client = AnilistApi()
    mongodb_client = MongoClient()
    transformer = sentence_transformers.SentenceTransformer(config["transformer_model"])
    
    # Repositories & Preprocessors Setup
    store = MongoDataStore(mongodb_client, db_name, batch_size)
    
    repos = {
        "tag": TagRepository(store),
        "genre": GenreRepository(store),
        "anime": MediaRepository(store, "anime"),
        "manga": MediaRepository(store, "manga"),
        "anime_recs": UserMediaRecommendationsRepository(store, "user_anime_recommendations"),
        "manga_recs": UserMediaRecommendationsRepository(store, "user_manga_recommendations")
    }
    
    pre = {
        "tag": TagPreprocessor(transformer),
        "genre": GenrePreprocessor(transformer),
        "media": MediaPreprocessor(repos["genre"], repos["tag"], transformer),
        "recs": UserMediaRecsPreprocessor()
    }

    # Pipeline Execution
    print("--- Starting ETL Database Population ---")
    
    etl_tags_job(api_client, repos["tag"], pre["tag"])
    etl_genres_job(api_client, repos["genre"], pre["genre"])
    
    etl_media_job(api_client, "anime", repos["anime"], repos["anime_recs"], pre["media"], pre["recs"])
    etl_media_job(api_client, "manga", repos["manga"], repos["manga_recs"], pre["media"], pre["recs"])
    
    print("--- ETL Process Finished ---")

if __name__ == "__main__":
    main()

