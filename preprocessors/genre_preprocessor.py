from sentence_transformers import SentenceTransformer

from models.genre import Genre


class GenrePreprocessor:

    def __init__(self, sentence_transformer: SentenceTransformer):
        self.sentence_transformer = sentence_transformer

    def preprocess(self, raw_genre_list: list):
        genre_list = []

        for genre in raw_genre_list:
            embedding = self.sentence_transformer.encode(genre)

            genre_list.append(Genre(genre, embedding))

        return genre_list
