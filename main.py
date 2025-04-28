import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

from external_apis.mal_api import MalApi
from preprocessors.user_preprocessors.mal_user_preprocessor import MalUserPreprocessor
from services.recommendation_service.media_list_filters.format_filter import FormatFilter
from services.recommendation_service.media_list_filters.genre_filter import GenreFilter
from services.recommendation_service.media_list_filters.score_filter import ScoreFilter
from services.recommendation_service.media_list_filters.year_filter import YearFilter
from services.recommendation_service.recommendation_engine import RecommendationEngine
from repositories.media_repository import MediaRepository
from routers import similarity_router, user_router
from services.recommendation_service.recommendation_service import RecommendationService
from services.recommendation_service.user_rec_profile_processor import UserRecProfileProcessor
from services.user_fetching_service.user_fetching_service import UserFetchingService
from preprocessors.user_preprocessors.anilist_user_preprocessor import AnilistUserPreprocessor
from external_apis.anilist_api import AnilistApi

@asynccontextmanager
async def lifespan(app: FastAPI):

    mongo_client = MongoClient()
    database_name = config["database_name"]

    anime_repository = MediaRepository(mongo_client, database_name, "anime")
    manga_repository = MediaRepository(mongo_client, database_name, "manga")

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
    app.state.mal_user_fetching_service = UserFetchingService(MalApi(), MalUserPreprocessor(anime_repository, manga_repository))

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

config = json.load(open("config.json"))
app = FastAPI(title="Anilist Recommender API", lifespan=lifespan)  # placeholder name

app.include_router(similarity_router.router)
app.include_router(user_router.router)

origins = [
    "http://localhost:5173"
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

if __name__ == "__main__":
    uvicorn.run(app)