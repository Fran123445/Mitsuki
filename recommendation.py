import numpy as np
from scipy.spatial.distance import cosine

from repositories.media_repository import MediaRepository
from repositories.tag_repository import TagRepository


class RecommendationEngine:

    def __init__(self,
                 media_repository: MediaRepository,
                 tag_repository: TagRepository):
        self.media_repository = media_repository
        self.tag_repository = tag_repository

    def extract_scores(self, user_anime_list: list) -> np.ndarray:
        """
        Extract scores from the user anime list.
        Replaces missing scores with the average score.

        Args:
            user_anime_list: List of user anime entries.

        Returns:
            A numpy array of scores.
        """
        scores = [user_anime.get("score") for user_anime in user_anime_list
                  if self.media_repository.get_media_by_id(user_anime["media"]["id"])]

        valid_scores = [s for s in scores if s != 0]
        avg_score = np.average(valid_scores)

        return np.array([s if s != 0 else avg_score for s in scores])

    def extract_vectors(
            self,
            user_anime_list: list,
            key: str
    ) -> np.ndarray:
        """
        Extracts vectors (like tags or genres) from each anime in the user list.

        Args:
            user_anime_list: List of user anime entries
            key: Key to extract from the anime data (eg "tags" or "genres")

        Returns:
            A numpy array where each row is the vector for that anime.
        """
        vectors = []

        for user_anime in user_anime_list:
            media = user_anime.get("media", {})
            anime_id = media.get("id")
            anime = self.media_repository.get_media_by_id(anime_id)

            if not anime:
                continue

            vector = np.array(getattr(anime, key))

            vectors.append(vector)

        return np.array(vectors)

    def compute_user_profiles(
            self,
            user_anime_list: list
    ):
        """
        Computes weighted average profiles for tags and genres.

        Args:
            user_anime_list: List of user anime entries.

        Returns:
            A tuple (tag_profile, genre_profile) (might change it later)
        """
        scores = self.extract_scores(user_anime_list)
        tag_vectors = self.extract_vectors(user_anime_list, key="media_embedding")
        genre_vectors = self.extract_vectors(user_anime_list, key="media_genres")

        tag_profile = np.average(tag_vectors, axis=0, weights=scores)
        genre_profile = np.average(genre_vectors, axis=0, weights=scores)

        return tag_profile, genre_profile

    def compute_cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        return 1 - cosine(vec_a, vec_b)

    def get_recommendations(self,
                            user_tag_profile: np.ndarray,
                            user_genre_profile: np.ndarray,
                            watched_anime_ids: set = None,
                            top_n: int = 25,
                            weight_genres: float = 0.5) -> list[tuple[str, float]]:
        """
        Retrieves the top recommendations by pondering both tag and genre similarities.

        Args:
            user_tag_profile: User's average tag vector.
            user_genre_profile: User's average genre vector.
            watched_anime_ids: List of anime IDs already watched (to exclude them).
            top_n: Amount of recommendations to return.
            weight_genres: Weighting factor for genre similarity. (not sure about this one either)

        Returns:
            A list of tuples (anime_title, combined_similarity_score).
        """
        watched_anime_ids = watched_anime_ids or {}
        recommendations = []

        for anime in self.media_repository.get_multiple_media({}, {"media_title": 1, "media_embedding": 1, "media_genres": 1, "media_id": 1}):
            if anime.media_id in watched_anime_ids:
                continue

            anime_embedding = anime.media_embedding
            anime_genres = anime.media_genres

            tag_similarity = self.compute_cosine_similarity(user_tag_profile, anime_embedding)
            genre_similarity = self.compute_cosine_similarity(user_genre_profile, anime_genres)

            # Combine similarities using a weighted average (might change it later)
            combined_similarity = (tag_similarity * (1 - weight_genres)) + (genre_similarity * weight_genres)
            recommendations.append((anime.media_title, combined_similarity))

        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:top_n]
