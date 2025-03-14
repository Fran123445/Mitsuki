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
