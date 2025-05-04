import json
import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from common.external_apis.anilist_api import AnilistApi
from common.external_apis.mal_api import MalApi
from common.preprocessors.user_preprocessors.anilist_user_preprocessor import AnilistUserPreprocessor
from common.preprocessors.user_preprocessors.mal_user_preprocessor import MalUserPreprocessor
from common.repositories.media_repository import MediaRepository
from web_service.routers import similarity_router, user_router
from web_service.services.recommendation_service.media_list_filters.format_filter import FormatFilter
from web_service.services.recommendation_service.media_list_filters.genre_filter import GenreFilter
from web_service.services.recommendation_service.media_list_filters.score_filter import ScoreFilter
from web_service.services.recommendation_service.media_list_filters.year_filter import YearFilter
from web_service.services.recommendation_service.recommendation_engine import RecommendationEngine
from web_service.services.recommendation_service.recommendation_service import RecommendationService
from web_service.services.recommendation_service.user_rec_profile_processor import UserRecProfileProcessor
from web_service.services.user_fetching_service.user_fetching_service import UserFetchingService

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    client_id = os.getenv("MAL_CLIENT_ID")
    mongo_uri = os.getenv("MONGO_URI")
    batch_size = int(os.getenv("MONGO_BATCH_SIZE"))

    mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    database_name = config["database_name"]

    anime_repository = MediaRepository(mongo_client, database_name, batch_size, "anime")
    manga_repository = MediaRepository(mongo_client, database_name, batch_size, "manga")

    recommendation_engine = RecommendationEngine()

    anime_user_rec_profile_processor = UserRecProfileProcessor("anime", anime_repository)
    manga_user_rec_profile_processor = UserRecProfileProcessor("manga", manga_repository)

    weight_genres = config["weight_genres"]

    year_filter = YearFilter()
    score_filter = ScoreFilter()
    genre_exclusion_filter = GenreFilter(True)
    genre_inclusion_filter = GenreFilter(False)
    format_filter = FormatFilter()

    filter_list = [year_filter, score_filter, genre_exclusion_filter,
                   genre_inclusion_filter, format_filter]

    app.state.anilist_user_fetching_service = UserFetchingService(AnilistApi(), AnilistUserPreprocessor())
    app.state.mal_user_fetching_service = UserFetchingService(MalApi(client_id), MalUserPreprocessor(anime_repository, manga_repository))

    app.state.anime_recommendation_service = RecommendationService(anime_repository,
                                                                   anime_user_rec_profile_processor,
                                                                   recommendation_engine,
                                                                   filter_list,
                                                                   weight_genres)

    app.state.manga_recommendation_service = RecommendationService(manga_repository,
                                                                   manga_user_rec_profile_processor,
                                                                   recommendation_engine,
                                                                   filter_list,
                                                                   weight_genres)

    yield

config = json.load(open("web_service/config.json"))
app = FastAPI(title="Anilist Recommender API", lifespan=lifespan)  # placeholder name

app.include_router(similarity_router.router)
app.include_router(user_router.router)

origins = [
    os.getenv("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Anilist Recommender API"}

@app.head("/")
def head():
    return None

if __name__ == "__main__":
    uvicorn.run(app)