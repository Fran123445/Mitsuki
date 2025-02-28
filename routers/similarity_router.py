from fastapi import APIRouter, Request

router = APIRouter(prefix="/similarity")


@router.get("/anime")
def get_top_similar_anime(anime_id: int, initial_year, final_year, request: Request, top_n: int = 10):
    params_dict = {"initial_year": int(initial_year),
                   "final_year": int(final_year),
                   }
    # Idk if it's unreasonable to handle this in the router

    return request.app.state.anime_recommendation_service.get_recommendations_from_media(anime_id, top_n, params_dict)
