from api import AnilistClient
from database import DatabaseClient
from recommendation import RecommendationEngine
def fill_database(db_client, api_client):
    if db_client.tags_collection.count_documents({}) == 0:
        tags = api_client.get_tags()
        db_client.insert_tags(tags)

    if db_client.genres_collection.count_documents({}) == 0:
        genres = api_client.get_genres()
        db_client.insert_genres(genres)

    if db_client.anime_collection.count_documents({}) == 0:
        for page in range(1, 201):
            anime_page = api_client.get_anime(page=page)
            db_client.insert_anime(anime_page)


if __name__ == '__main__':
    api_client = AnilistClient()
    db_client = DatabaseClient()
    recommender = RecommendationEngine(db_client)

    username = input("Input username: ")

    user_anime_list = api_client.get_user_completed_list(username)
    tag_profile, genre_profile = recommender.compute_user_profiles(user_anime_list)

    watched_anime_list = [anime["media"]["id"] for anime in user_anime_list]

    recs = recommender.get_recommendations(tag_profile, genre_profile, watched_anime_list, weight_genres=0.5)

    for idx, anime in enumerate(recs):
        print(f"{idx+1} - {anime[0]}: {anime[1]:.2f}")
