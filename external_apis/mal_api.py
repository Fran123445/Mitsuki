from dotenv import load_dotenv

from external_apis.external_api import ExternalApi
import requests
import os

class MalApi(ExternalApi):

    load_dotenv()
    BASE_API_URL = "https://api.myanimelist.net/v2"
    BASE_SITE_URL = "https://myanimelist.net"
    client_id = os.getenv("MAL_CLIENT_ID")

    def _fetch_user_avatar(self, username):
        url = f"https://api.jikan.moe/v4/users/{username}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("images", {}).get("jpg", {}).get("image_url", None)
            # i hate my life
        
        return None
    
    def _fetch_media_list(self, username, media_type, status, headers):
        url = f"{self.BASE_API_URL}/users/{username}/{media_type}list?status={status}&limit=1000&fields=id,list_status{{score}}"
        response = requests.get(url, headers=headers)
        return response.json()
    
    def _format_user_data(self, username, avatar_url, anime_data, manga_data, 
                         planned_anime_data, planned_manga_data):
        return {
            "User": {
                "username": username,
                "avatar_url": avatar_url
            },
            "anime": [
                    {"mediaId": item["node"]["id"], "score": item["list_status"]["score"]}
                    for item in anime_data.get("data", [])
                ],
            "manga": [
                    {"mediaId": item["node"]["id"], "score": item["list_status"]["score"]}
                    for item in manga_data.get("data", [])
                ],
            "planned_anime": [
                    {"mediaId": item["node"]["id"]}
                    for item in planned_anime_data.get("data", [])
                ],
            "planned_manga": [
                    {"mediaId": item["node"]["id"]}
                    for item in planned_manga_data.get("data", [])
                ]
        }

    def get_user_data(self, username):
        headers = {
            "X-MAL-CLIENT-ID": self.client_id,
        }
        
        user_data = self._fetch_user_avatar(username)
        anime_data = self._fetch_media_list(username, "anime", "completed", headers)
        manga_data = self._fetch_media_list(username, "manga","completed", headers)
        planned_anime_data = self._fetch_media_list(username, "anime", "plan_to_watch", headers)
        planned_manga_data = self._fetch_media_list(username, "manga", "plan_to_read", headers)
        
        return self._format_user_data(username, user_data, anime_data, manga_data, 
                                     planned_anime_data, planned_manga_data)
