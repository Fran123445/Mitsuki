from fastapi import APIRouter, Request

router = APIRouter(prefix="/similarity")

@router.get("/anime")
def get_top_similar_anime(anime_id: int, request: Request, top_n: int = 10):
    # will later refactor this into a service
    anime = request.app.state.anime_repository.get_media_by_id(anime_id)
    tag_profile = anime.media_embedding
    genre_profile = anime.media_genres

    return request.app.state.recommender.get_recommendations(tag_profile, genre_profile, weight_genres=0.33, top_n=top_n+1)[1:]