import numpy as np
from scipy.spatial.distance import cdist


class RecommendationEngine:

    def get_recommendations(self,
                            media_list: list,
                            tag_profile: np.ndarray,
                            genre_profile: np.ndarray,
                            weight_genres: float = 0.5) -> list[tuple[str, float]]:
        """
        Retrieves the top recommendations by pondering both tag and genre similarities.

        Args:
            media_list: List of media entries,
            tag_profile: Tag vector.
            genre_profile: Genre vector.
            weight_genres: Weighting factor for genre similarity. (not sure about this one either)

        Returns:
            A list of tuples (media_title, combined_similarity_score).
        """

        media_ids = [media.id for media in media_list]

        media_tag_embeddings = np.array([media.tag_embedding for media in media_list])
        media_genres_embeddings = np.array([media.genre_embedding for media in media_list])

        tag_profile = tag_profile.reshape(1, -1)  # Reshape to 2D array for performing cosine similarity
        genre_profile = genre_profile.reshape(1, -1)

        tag_similarities = 1 - cdist(tag_profile, media_tag_embeddings, "cosine").flatten()  # Flattens back to 1D array
        genre_similarities = 1 - cdist(genre_profile, media_genres_embeddings, "cosine").flatten()

        combined_similarities = weight_genres * genre_similarities + (1 - weight_genres) * tag_similarities

        recommendations = list(zip(media_ids, combined_similarities))

        recommendations = [(id, similarity) for (id, similarity) in recommendations if not np.isnan(similarity)]

        recommendations.sort(key=lambda x: x[1], reverse=True)

        return recommendations
