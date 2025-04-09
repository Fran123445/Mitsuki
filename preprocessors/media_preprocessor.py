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

    def _get_tag_embedding(self, tag_dict):
        # If no tags are active, return a zero vector (might not be ideal but IDK)
        if not tag_dict:
            return np.zeros(self.sentence_transformer.get_sentence_embedding_dimension())

        embeddings = []
        weights = []

        for id, rank in tag_dict.items():
            tag = self.tag_repository.get_tag_by_id(id)
            embeddings.append(tag.embedding)
            weights.append(rank)

        return np.average(np.array(embeddings), axis=0, weights=np.array(weights))

    def preprocess(self, raw_media_list: list[dict]):
        genres_size = self.genre_repository.get_total_amount()

        media_list = []

        for raw_media_dict in raw_media_list:
            tag_dict = {}

            # Create feature vectors
            genre_features = np.zeros(genres_size)

            # Process tags
            for tag in raw_media_dict.get('tags'):
                tag_dict[tag["id"]] = tag["rank"]

            # Process genres
            for genre in raw_media_dict.get('genres', []):
                genre_object = self.genre_repository.get_genre_by_name(genre)
                genre_features[genre_object.index] = 1

            tag_embedding = self._get_tag_embedding(tag_dict)

            media_list.append(Media(
                raw_media_dict['id'],
                raw_media_dict['idMal'],
                raw_media_dict['title']['romaji'],
                raw_media_dict['title']['english'],
                genre_features,
                tag_dict,
                raw_media_dict.get('description', ''),
                tag_embedding,
                raw_media_dict['coverImage']['large'],
                raw_media_dict['startDate']['year'],
                raw_media_dict.get('meanScore', 0),
                raw_media_dict.get('popularity', 0),
                raw_media_dict.get('isAdult', False),
                raw_media_dict.get('format')
            ))

        return media_list
