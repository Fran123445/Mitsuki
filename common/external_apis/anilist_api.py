import requests
from ratelimit import limits, sleep_and_retry

from common.external_apis.external_api import ExternalApi


class AnilistApi(ExternalApi):
    BASE_URL = 'https://graphql.anilist.co'

    @sleep_and_retry
    @limits(calls=85, period=60)
    def query(self, query: str, variables: dict = None) -> dict:
        json_data = {"query": query}
        if variables:
            json_data["variables"] = variables
        response = requests.post(self.BASE_URL, json=json_data)
        response.raise_for_status()
        return response.json()

    def get_tags(self) -> list:
        query = """
           query {
             MediaTagCollection {
               id
               name
             }
           }
           """
        data = self.query(query)
        return data["data"]["MediaTagCollection"]

    def get_genres(self) -> list:
        query = """
        query {
          GenreCollection
        }
        """
        data = self.query(query)
        return data["data"]["GenreCollection"]

    def get_anime(self, page: int, recs_per_page: int) -> list:
        query = """
        query ($page: Int, $recsPerPage: Int, $recsSort: [RecommendationSort]) {
          Page(page: $page, perPage: 50) {
            media(sort: POPULARITY_DESC, type: ANIME, format_in: [TV, MOVIE, OVA, ONA, TV_SHORT],
                  status_in: [FINISHED, RELEASING]) {
              id
              idMal
              title {
                english
                romaji
              }
              genres
              tags {
                id
                rank
              }
              coverImage {
                large
              }
              description
              startDate {
                year
              }
              meanScore
              popularity
              isAdult
              format
              recommendations(perPage: $recsPerPage, sort: $recsSort) {
                edges {
                  node {
                    mediaRecommendation {
                      id
                      title {
                        romaji
                      }
                    }
                    rating
                  }
                }
              }
            }
          }
        }
        """
        variables = {"page": page, "recsPerPage": recs_per_page, "recsSort": "RATING_DESC"}
        data = self.query(query, variables)
        return data["data"]["Page"]["media"]

    def get_manga(self, page: int, recs_per_page: int):
        query = """
                query ($page: Int, $recsPerPage: Int, $recsSort: [RecommendationSort]) {
                  Page(page: $page, perPage: 50) {
                    media(sort: POPULARITY_DESC, type: MANGA,
                          status_in: [FINISHED, RELEASING]) {
                      id
                      idMal
                      title {
                        english
                        romaji
                      }
                      genres
                      tags {
                        id
                        rank
                      }
                      coverImage {
                        large
                      }
                      description
                      startDate {
                        year
                      }
                      meanScore
                      popularity
                      isAdult
                      format
                      recommendations(perPage: $recsPerPage, sort: $recsSort) {
                        edges {
                          node {
                            mediaRecommendation {
                              id
                              title {
                                romaji
                              }
                            }
                            rating
                          }
                        }
                      }
                    }
                  }
                }
                """
        variables = {"page": page, "recsPerPage": recs_per_page, "recsSort": "RATING_DESC"}
        data = self.query(query, variables)
        return data["data"]["Page"]["media"]

    def get_user_data(self, username: str) -> list:
        query = """
        query($userName: String) {
          User(name: $userName) {
            name
            avatar {
              medium
            }
          },
          anime: MediaListCollection(userName: $userName, type: ANIME, status: COMPLETED) {
            lists {
              entries {
                mediaId
                score(format: POINT_100)
              }
            }
          },
          manga: MediaListCollection(userName:  $userName, type: MANGA, status: COMPLETED) {
            lists {
              entries {
                mediaId
                score(format: POINT_100)
              }
            },
          },
          planned_anime: MediaListCollection(userName:  $userName, type: ANIME, status: PLANNING) {
            lists {
              entries {
                mediaId
              }
            }
          },
          planned_manga: MediaListCollection(userName:  $userName, type: MANGA, status: PLANNING) {
            lists {
              entries {
                mediaId
              }
            }
          },
        }
        """
        variables = {"userName": username}
        data = self.query(query, variables)

        return data["data"]