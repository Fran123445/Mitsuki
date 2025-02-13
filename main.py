from pymongo import MongoClient
import requests
import numpy as np
from scipy.spatial.distance import cosine


def get_tags():
    query = """
        query {
          MediaTagCollection {
            id
            name
          }
        }
        """
    url = 'https://graphql.anilist.co'
    json_data = {
        'query': query
    }
    response = requests.post(url=url, json=json_data)

    tags = response.json()["data"]["MediaTagCollection"]

    idx = 0
    for tag in tags:
        tag["index"] = idx
        tags_collection.insert_one(tag)
        idx += 1


def get_genres():
    query = """
        query {
          GenreCollection
        }
        """
    url = 'https://graphql.anilist.co'
    json_data = {
        'query': query
    }
    response = requests.post(url=url, json=json_data)

    genres = response.json()["data"]["GenreCollection"]

    idx = 0

    for genre in genres:
        genre_json = {"name": genre, "index": idx}
        genre_collection.insert_one(genre_json)
        idx += 1


def get_anime(page):
    query = """
        query {
          Page(page:""" + str(page) + """, perPage: 50) {
            media(sort: POPULARITY_DESC, type: ANIME, format_in: [TV, MOVIE, OVA, ONA]) {
              id
              title {
                romaji
              }
              genres
              tags {
                  id
                  rank
              }
              description
            }
          }
        }
        """

    url = 'https://graphql.anilist.co'
    json_data = {
        'query': query
    }
    response = requests.post(url=url, json=json_data)
    print(response)

    tags_size = tags_collection.count_documents({})
    genres_size = genre_collection.count_documents({})

    medias = response.json()["data"]["Page"]["media"]

    for media in medias:
        tag_ranks = np.zeros(tags_size)
        genre_features = np.zeros(genres_size)

        # Process tags
        for tag in media.get('tags', []):
            tag_doc = tags_collection.find_one({'id': tag['id']})
            if tag_doc:
                tag_ranks[tag_doc['index']] = tag.get('rank', 0)

        # Process genres
        for genre in media.get('genres', []):
            genre_doc = genre_collection.find_one({'name': genre})
            if genre_doc:
                genre_features[genre_doc['index']] = 1  # Binary presence indicator

        anime = {
            'id': media['id'],
            'title': media['title']['romaji'],
            'genres': genre_features.tolist(),
            'tags': tag_ranks.tolist(),
            'description': media['description']
        }

        anime_collection.insert_one(anime)


def get_user(username):
    query = """query {
            MediaListCollection(userName: \"""" + str(username) + """\", type: ANIME, status: COMPLETED) {
            lists {
              entries {
                media {
                  id
                  title {
                    userPreferred
                  }
                }
                score (format: POINT_10)
              }
            }
          }
          }
            """

    url = 'https://graphql.anilist.co'
    json_data = {
        'query': query
    }
    response = requests.post(url=url, json=json_data)

    user = {"list": [], "weights": []}

    media_collection = response.json()["data"]["MediaListCollection"]["lists"][0]["entries"]
    average_score = np.average([media["score"] for media in media_collection])

    for media in media_collection:
        anime = anime_collection.find_one({"id": media["media"]["id"]})
        if not anime:
            print(media["media"]["title"]["userPreferred"] + " not found")
            continue

        user["list"].append(anime)

        if media["score"]:
            user["weights"].append(media["score"])
        else:
            user["weights"].append(average_score)

    return user


def average_tag(user):
    weights = np.array(user["weights"])
    tags = np.array([anime["tags"] for anime in user["list"]])

    return np.average(tags, axis=0, weights=weights)


def get_best_matching_anime_from_collection(user_avg_tags, anime_collection, watched_anime_ids):
    anime_similarities = []
    watched_anime_ids = watched_anime_ids or []

    for anime in anime_collection.find({}, {"title": 1, "tags": 1, "id": 1}):
        anime_id = anime['id']

        if anime_id in watched_anime_ids:
            continue

        anime_tags = np.array(anime['tags'])
        similarity = 1 - cosine(user_avg_tags, anime_tags)
        anime_similarities.append((anime['title'], similarity))

    anime_similarities.sort(key=lambda x: x[1], reverse=True)

    return anime_similarities[:25]


if __name__ == '__main__':
    client = MongoClient()

    db = client["AnilistData"]
    tags_collection = db["tags"]
    genre_collection = db["genres"]
    anime_collection = db["anime"]

    username = input("Input username: ")

    user = get_user(username)
    average_tags = average_tag(user)
    watched_anime = [anime["id"] for anime in user["list"]]
    i = 1
    for anime in get_best_matching_anime_from_collection(average_tags, anime_collection, watched_anime):
        print(f"{i} {anime[0]}: {anime[1]}")
        i += 1
