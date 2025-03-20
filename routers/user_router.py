
from fastapi import APIRouter, Request

router = APIRouter(prefix="/user")

@router.get("/")
def get_user_name_and_avatar(username: str, request: Request):
    return request.app.state.user_fetching_service.fetch_user_avatar(username)