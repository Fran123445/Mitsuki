import numpy as np

from models.user.user import User
from repositories.media_repository import MediaRepository


class UserRecProfileProcessor():

    def __init__(self,
                 media_type: str,
                 media_repository: MediaRepository):
        self.media_type = media_type
        self.media_repository = media_repository

    def _extract_scores(self,
                        user_media_list: list,
                        tipping_point: int) -> np.ndarray:
        """
        Extract scores from the user media list.

        Args:
            user_media_list: List of user media entries.

        Returns:
            A numpy array of scores.
        """
        scores = [media_entry.score for media_entry in user_media_list
                  if self.media_repository.get_media_by_id(media_entry.id)]

        return np.array([s if s != 0 else tipping_point for s in scores])

    def _extract_vectors(
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

        for media_entry in user_media_list:
            media_id = media_entry.id
            media = self.media_repository.get_media_by_id(media_id)

            if not media:
                continue

            vector = np.array(getattr(media, key))

            vectors.append(vector)

        return np.array(vectors)

    def get_media_list(self, user: User):
        if self.media_type == "anime":
            user_media_list = user.watched_anime
        elif self.media_type == "manga":
            user_media_list = user.read_manga

        return user_media_list

    def compute_user_profiles(
            self,
            user: User,
            tipping_point: int = 50
    ):
        """
        Computes weighted average profiles for tags and genres.

        Args:
            user: a user.
            tipping_point: whatever the user consider a neutral score

        Returns:
            A tuple (tag_profile, genre_profile)
        """

        user_media_list = self.get_media_list(user)

        scores = self._extract_scores(user_media_list, tipping_point) - tipping_point

        tag_vectors = self._extract_vectors(user_media_list, "tag_embedding")
        genre_vectors = self._extract_vectors(user_media_list, "genre_embedding")

        scores_reshaped = scores.reshape(1, len(scores))  # numpy yells at me due to not being able to broadcast otherwise

        tag_product = np.dot(scores_reshaped, tag_vectors)
        genre_product = np.dot(scores_reshaped, genre_vectors)

        denominator = np.sum(np.abs(scores))

        return (tag_product / denominator), (genre_product / denominator)