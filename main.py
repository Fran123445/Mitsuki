import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

from repositories.genre_repository import GenreRepository
from services.recommendation_service.media_list_filters.format_filter import FormatFilter
from services.recommendation_service.media_list_filters.genre_filter import GenreFilter
from services.recommendation_service.media_list_filters.score_filter import ScoreFilter
from services.recommendation_service.media_list_filters.year_filter import YearFilter
from services.recommendation_service.recommendation_engine import RecommendationEngine
from repositories.media_repository import MediaRepository
from repositories.tag_repository import TagRepository
from routers import similarity_router, user_router
from services.recommendation_service.recommendation_service import RecommendationService
from services.user_fetching_service.user_fetching_service import UserFetchingService
from preprocessors.user_preprocessor import UserPreprocessor
from api import AnilistClient

@asynccontextmanager
async def lifespan(app: FastAPI):

    mongo_client = MongoClient()
    database_name = config["database_name"]

    tag_repository = TagRepository(mongo_client, database_name)
    genre_repository = GenreRepository(mongo_client, database_name)
    anime_repository = MediaRepository(mongo_client, database_name, "anime")
    manga_repository = MediaRepository(mongo_client, database_name, "manga")

    anime_recommender = RecommendationEngine(anime_repository, tag_repository)
    manga_recommender = RecommendationEngine(manga_repository, tag_repository)

    weight_genres = config["weight_genres"]

    year_filter = YearFilter()
    score_filter = ScoreFilter()
    genre_exclusion_filter = GenreFilter(genre_repository, True)
    genre_inclusion_filter = GenreFilter(genre_repository, False)
    format_filter = FormatFilter()

    filter_list = [year_filter, score_filter, genre_exclusion_filter,
                   genre_inclusion_filter, format_filter]

    app.state.user_fetching_service = UserFetchingService(AnilistClient(), UserPreprocessor())

    app.state.anime_recommendation_service = RecommendationService(anime_repository,
                                                                   anime_recommender,
                                                                   filter_list,
                                                                   weight_genres)

    app.state.manga_recommendation_service = RecommendationService(manga_repository,
                                                                   manga_recommender,
                                                                   filter_list,
                                                                   weight_genres)

    yield

config = json.load(open("config.json"))
app = FastAPI(title="Anilist Recommender API", lifespan=lifespan)  # placeholder name

app.include_router(similarity_router.router)
app.include_router(user_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Anilist Recommender API"}

if __name__ == "__main__":
    uvicorn.run(app)