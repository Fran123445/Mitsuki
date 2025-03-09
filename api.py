import requests

class AnilistClient:
    BASE_URL = 'https://graphql.anilist.co'

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

    def get_anime(self, page: int) -> list:
        query = """
        query ($page: Int) {
          Page(page: $page, perPage: 50) {
            media(sort: POPULARITY_DESC, type: ANIME, format_in: [TV, MOVIE, OVA, ONA],
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
            }
          }
        }
        """
        variables = {"page": page}
        data = self.query(query, variables)
        return data["data"]["Page"]["media"]

    def get_user_completed_list(self, username: str) -> list:
        query = """
        query ($username: String) {
          MediaListCollection(userName: $username, type: ANIME, status: COMPLETED) {
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
        variables = {"username": username}
        data = self.query(query, variables)

        return data["data"]["MediaListCollection"]["lists"][0]["entries"]