import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import MongoClient

from api import AnilistClient
from services.recommendation_service.recommendation_engine import RecommendationEngine
from repositories.genre_repository import GenreRepository
from repositories.media_repository import MediaRepository
from repositories.tag_repository import TagRepository
from routers import similarity_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    api_client = AnilistClient()

    mongo_client = MongoClient()
    database_name = config["database_name"]

    tag_repository = TagRepository(mongo_client, database_name)
    genre_repository = GenreRepository(mongo_client, database_name)
    anime_repository = MediaRepository(mongo_client, database_name, "anime")

    app.state.tag_repository = tag_repository
    app.state.genre_repository = genre_repository
    app.state.anime_repository = anime_repository
    app.state.recommender = RecommendationEngine(anime_repository, tag_repository)

    yield


config = json.load(open("config.json"))
app = FastAPI(title="Anilist Recommender API", lifespan=lifespan)  # placeholder name

app.include_router(similarity_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Anilist Recommender API"}
