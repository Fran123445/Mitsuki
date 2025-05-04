import numpy as np
from sentence_transformers import SentenceTransformer

from common.models.media import Media
from common.repositories.genre_repository import GenreRepository
from common.repositories.tag_repository import TagRepository


class MediaPreprocessor:

    def __init__(self,
                 genre_repository: GenreRepository,
                 tag_repository: TagRepository,
                 sentence_transformer: SentenceTransformer):
        self.genre_repository = genre_repository
        self.tag_repository = tag_repository
        self.sentence_transformer = sentence_transformer

    def _get_tag_embedding(self, tag_dict: dict):
        # If no tags, return a zero vector (might not be ideal but IDK)
        if not tag_dict:
            return np.zeros(self.sentence_transformer.get_sentence_embedding_dimension())

        embeddings = []
        weights = []

        for name, rank in tag_dict.items():
            tag = self.tag_repository.get_tag_by_name(name)
            embeddings.append(tag.embedding)
            weights.append(rank)

        return np.average(np.array(embeddings), axis=0, weights=np.array(weights))

    def _get_genre_embedding(self, genre_list: list):
        if not genre_list:
            return np.zeros(self.sentence_transformer.get_sentence_embedding_dimension())

        embeddings = []

        for genre_name in genre_list:
            genre = self.genre_repository.get_genre_by_name(genre_name)
            embeddings.append(genre.embedding)

        return np.average(embeddings, axis=0)

    def preprocess(self, raw_media_list: list[dict]):

        media_list = []

        for raw_media_dict in raw_media_list:
            tag_dict = {}

            # Process tags
            for tag_data in raw_media_dict.get('tags'):
                tag = self.tag_repository.get_tag_by_id(tag_data["id"])
                tag_dict[tag.name] = tag_data["rank"]

            tag_embedding = self._get_tag_embedding(tag_dict)

            # Process genres
            genres = raw_media_dict.get("genres", [])

            genre_embedding = self._get_genre_embedding(genres)

            media_list.append(Media(
                raw_media_dict['id'],
                raw_media_dict['idMal'],
                raw_media_dict['title']['romaji'],
                raw_media_dict['title']['english'],
                set(genres),
                tag_dict,
                raw_media_dict.get('description', ''),
                tag_embedding,
                genre_embedding,
                raw_media_dict['coverImage']['large'],
                raw_media_dict['startDate']['year'],
                raw_media_dict.get('meanScore', 0),
                raw_media_dict.get('popularity', 0),
                raw_media_dict.get('isAdult', False),
                raw_media_dict.get('format')
            ))

        return media_list
