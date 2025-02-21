from fastapi import APIRouter, Request

router = APIRouter(prefix="/similarity")

@router.get("/anime")
def get_top_similar_anime(anime_id: int, request: Request, top_n: int = 10):
    return request.app.state.anime_recommendation_service.get_recommendations_from_media(anime_id, top_n)