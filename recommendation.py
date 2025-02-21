import numpy as np
from scipy.spatial.distance import cdist

from repositories.media_repository import MediaRepository
from repositories.tag_repository import TagRepository


class RecommendationEngine:

    def __init__(self,
                 media_repository: MediaRepository,
                 tag_repository: TagRepository):
        self.media_repository = media_repository
        self.tag_repository = tag_repository

    def extract_scores(self, user_media_list: list) -> np.ndarray:
        """
        Extract scores from the user media list.
        Replaces missing scores with the average score.

        Args:
            user_media_list: List of user media entries.

        Returns:
            A numpy array of scores.
        """
        scores = [user_media.get("score") for user_media in user_media_list
                  if self.media_repository.get_media_by_id(user_media["media"]["id"])]

        valid_scores = [s for s in scores if s != 0]
        avg_score = np.average(valid_scores)

        return np.array([s if s != 0 else avg_score for s in scores])

    def extract_vectors(
            self,
            user_media_list: list,
            key: str
    ) -> np.ndarray:
        """
        Extracts vectors (like tags or genres) from each media in the user list.

        Args:
            user_media_list: List of user media entries
            key: Key to extract from the media data (eg "tags" or "genres")

        Returns:
            A numpy array where each row is the vector for that media.
        """
        vectors = []

        for user_media in user_media_list:
            media = user_media.get("media", {})
            media_id = media.get("id")
            media = self.media_repository.get_media_by_id(media_id)

            if not media:
                continue

            vector = np.array(getattr(media, key))

            vectors.append(vector)

        return np.array(vectors)

    def compute_user_profiles(
            self,
            user_media_list: list
    ):
        """
        Computes weighted average profiles for tags and genres.

        Args:
            user_media_list: List of user media entries.

        Returns:
            A tuple (tag_profile, genre_profile) (might change it later)
        """
        scores = self.extract_scores(user_media_list)
        tag_vectors = self.extract_vectors(user_media_list, key="media_embedding")
        genre_vectors = self.extract_vectors(user_media_list, key="media_genres")

        tag_profile = np.average(tag_vectors, axis=0, weights=scores)
        genre_profile = np.average(genre_vectors, axis=0, weights=scores)

        return tag_profile, genre_profile

    def get_recommendations(self,
                            user_tag_profile: np.ndarray,
                            user_genre_profile: np.ndarray,
                            watched_media_ids: set = None,
                            top_n: int = 25,
                            weight_genres: float = 0.5) -> list[tuple[str, float]]:
        """
        Retrieves the top recommendations by pondering both tag and genre similarities.

        Args:
            user_tag_profile: User's average tag vector.
            user_genre_profile: User's average genre vector.
            watched_media_ids: List of media IDs already watched (to exclude them).
            top_n: Amount of recommendations to return.
            weight_genres: Weighting factor for genre similarity. (not sure about this one either)

        Returns:
            A list of tuples (media_title, combined_similarity_score).
        """
        watched_media_ids = watched_media_ids or set()

        media_list = self.media_repository.get_multiple_media({}, {"media_title_romaji": 1, "media_embedding": 1, "media_genres": 1, "media_id": 1})
        media_list = [media for media in media_list if media.media_id not in watched_media_ids]

        media_titles = [media.media_title_romaji for media in media_list]

        media_tag_embeddings = np.array([media.media_embedding for media in media_list])
        media_genres = np.array([media.media_genres for media in media_list])

        user_tag_profile = user_tag_profile.reshape(1, -1)  # Reshape to 2D array for performing cosine similarity
        user_genre_profile = user_genre_profile.reshape(1, -1)

        tag_similarities = 1 - cdist(user_tag_profile, media_tag_embeddings, "cosine").flatten()  # Flattens back to 1D array
        genre_similarities = 1 - cdist(user_genre_profile, media_genres, "cosine").flatten()

        combined_similarities = weight_genres * genre_similarities + (1 - weight_genres) * tag_similarities

        recommendations = list(zip(media_titles, combined_similarities))

        recommendations.sort(key=lambda x: x[1], reverse=True)

        return recommendations[:top_n]
