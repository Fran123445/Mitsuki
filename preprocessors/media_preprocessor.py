import numpy as np
from sentence_transformers import SentenceTransformer

from models.media import Media
from repositories.genre_repository import GenreRepository
from repositories.tag_repository import TagRepository


class MediaPreprocessor:

    def __init__(self,
                 genre_repository: GenreRepository,
                 tag_repository: TagRepository,
                 sentence_transformer: SentenceTransformer):
        self.genre_repository = genre_repository
        self.tag_repository = tag_repository
        self.sentence_transformer = sentence_transformer

    def _get_anime_embedding(self, tag_ranks):
        # Find the indices where the tag weight is greater than zero
        active_indices = [i for i, weight in enumerate(tag_ranks) if weight > 0]

        # If no tags are active, return a zero vector (might not be ideal but IDK)
        if not active_indices:
            return np.zeros(self.sentence_transformer.get_sentence_embedding_dimension())

        tags = []

        for index in active_indices:
            tags.append(self.tag_repository.get_tag_by_index(index))

        # Prepare lists for embeddings and their corresponding weights.
        embeddings = []
        weights = []

        # Create a mapping from tag index to its weight in the anime document.
        weight_map = {i: tag_ranks[i] for i in active_indices}

        for tag in tags:
            idx = tag.index
            embeddings.append(tag.embedding)
            weights.append(weight_map[idx])

        return np.average(np.array(embeddings), axis=0, weights=np.array(weights))

    def preprocess(self, raw_media_list: list[dict]):
        tags_size = self.tag_repository.get_total_amount()
        genres_size = self.genre_repository.get_total_amount()

        media_list = []

        for raw_media_dict in raw_media_list:
            # Create feature vectors
            tag_ranks = np.zeros(tags_size)
            genre_features = np.zeros(genres_size)

            # Process tags
            for tag in raw_media_dict.get('tags'):
                tag_object = self.tag_repository.get_tag_by_id(tag['id'])
                tag_ranks[tag_object.index] = tag.get('rank', 0)

            # Process genres
            for genre in raw_media_dict.get('genres', []):
                genre_object = self.genre_repository.get_genre_by_name(genre)
                genre_features[genre_object.index] = 1

            embedding = self._get_anime_embedding(tag_ranks)

            media_list.append(Media(
                raw_media_dict['id'],
                raw_media_dict['title']['romaji'],
                genre_features,
                tag_ranks,
                raw_media_dict.get('description', ''),
                embedding,
            ))

        return media_list
