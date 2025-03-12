import json
from contextlib import asynccontextmanager

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
from routers import similarity_router
from services.recommendation_service.recommendation_service import RecommendationService


@asynccontextmanager
async def lifespan(app: FastAPI):

    mongo_client = MongoClient()
    database_name = config["database_name"]

    tag_repository = TagRepository(mongo_client, database_name)
    genre_repository = GenreRepository(mongo_client, database_name)
    anime_repository = MediaRepository(mongo_client, database_name, "anime")

    anime_recommender = RecommendationEngine(anime_repository, tag_repository)

    year_filter = YearFilter()
    score_filter = ScoreFilter()
    genre_exclusion_filter = GenreFilter(genre_repository, True)
    genre_inclusion_filter = GenreFilter(genre_repository, False)
    format_filter = FormatFilter()

    app.state.anime_recommendation_service = RecommendationService(anime_repository,
                                                                   anime_recommender,
                                                                   [year_filter, score_filter, genre_exclusion_filter,
                                                                    genre_inclusion_filter, format_filter],
                                                                   config["weight_genres"])

    yield

config = json.load(open("config.json"))
app = FastAPI(title="Anilist Recommender API", lifespan=lifespan)  # placeholder name

app.include_router(similarity_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Anilist Recommender API"}