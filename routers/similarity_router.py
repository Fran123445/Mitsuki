from typing import Annotated

from fastapi import APIRouter, Request, Query, Depends

router = APIRouter(prefix="/similarity")

def common_params(
    top_n: int = 10,
    initial_year: int = 1900,
    final_year: int = 2025,
    minimum_score: int = 0,
    maximum_score: int = 100,
    excluded_genres: Annotated[list, Query()] = [],
    included_genres: Annotated[list, Query()] = [],
    formats: Annotated[list, Query()] = [],
):
    return {
        "top_n": top_n,
        "initial_year": initial_year,
        "final_year": final_year,
        "minimum_score": minimum_score,
        "maximum_score": maximum_score,
        "excluded_genres": excluded_genres,
        "included_genres": included_genres,
        "formats": formats,
    }

@router.get("/anime")
def get_top_similar_anime(id: int, request: Request, params: dict = Depends(common_params)):
    return request.app.state.anime_recommendation_service.get_recommendations_from_media(id, params["top_n"], params)

@router.get("/manga")
def get_top_similar_manga(id: int, request: Request, params: dict = Depends(common_params)):
    return request.app.state.manga_recommendation_service.get_recommendations_from_media(id, params["top_n"], params)

@router.get("/user/anime")
def get_user_anime(username: str, platform: str, request: Request, params: dict = Depends(common_params)):
    return _get_user_recommendations(username, platform, request, params, "anime")

@router.get("/user/manga")
def get_user_manga(username: str, platform: str, request: Request, params: dict = Depends(common_params)):
    return _get_user_recommendations(username, platform, request, params, "manga")

def _get_user_recommendations(username: str, platform: str, request: Request, params: dict, media_type: str):
    if platform == "anilist":
        user_data = request.app.state.anilist_user_fetching_service.fetch_user_data(username)
    elif platform == "myanimelist":
        user_data = request.app.state.mal_user_fetching_service.fetch_user_data(username)
    else:
        raise ValueError(f"Unsupported platform: {platform}")

    if media_type == "anime":
        watched_media = user_data.watched_anime
        params["planned_media"] = user_data.planned_anime
        return request.app.state.anime_recommendation_service.get_recommendations_from_user(watched_media,
                                                                                            params["top_n"], params)
    elif media_type == "manga":
        watched_media = user_data.read_manga
        params["planned_media"] = user_data.planned_manga
        return request.app.state.manga_recommendation_service.get_recommendations_from_user(watched_media,
                                                                                            params["top_n"], params)
    else:
        raise ValueError(f"Unsupported media type: {media_type}")