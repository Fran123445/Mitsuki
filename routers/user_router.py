
from fastapi import APIRouter, Request

router = APIRouter(prefix="/user")

@router.get("/anilist")
def get_anilist_user_name_and_avatar(username: str, request: Request):
    return request.app.state.anilist_user_fetching_service.fetch_user_avatar(username)

@router.get("/myanimelist")
def get_mal_user_name_and_avatar(username: str, request: Request):
    return request.app.state.mal_user_fetching_service.fetch_user_avatar(username)