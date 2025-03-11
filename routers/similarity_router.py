from typing import Annotated

from fastapi import APIRouter, Request, Query

router = APIRouter(prefix="/similarity")


@router.get("/anime")
def get_top_similar_anime(id: int, request: Request, top_n: int = 10,  initial_year: int = 1900,
                          final_year: int =2025, minimum_score: int = 0, maximum_score: int = 100,
                          excluded_genres: Annotated[list, Query()] = []):
    params_dict = {"initial_year": initial_year,
                   "final_year": final_year,
                   "minimum_score": minimum_score,
                   "maximum_score": maximum_score,
                   "excluded_genres": excluded_genres
                   }
    # Idk if it's unreasonable to handle this in the router

    return request.app.state.anime_recommendation_service.get_recommendations_from_media(id, top_n, params_dict)
