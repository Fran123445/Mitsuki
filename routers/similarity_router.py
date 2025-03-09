from fastapi import APIRouter, Request

router = APIRouter(prefix="/similarity")


@router.get("/anime")
def get_top_similar_anime(id: int, request: Request, top_n: int = 10,  initial_year=1900, final_year=2025, minimum_score=0, maximum_score=100):
    params_dict = {"initial_year": int(initial_year),
                   "final_year": int(final_year),
                   "minimum_score": int(minimum_score),
                   "maximum_score": int(maximum_score),
                   }
    # Idk if it's unreasonable to handle this in the router

    return request.app.state.anime_recommendation_service.get_recommendations_from_media(id, top_n, params_dict)
