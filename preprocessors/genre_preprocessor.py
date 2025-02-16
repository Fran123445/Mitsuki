from models.genre import Genre


class GenrePreprocessor:

    def preprocess(self, raw_genre_list: list):
        genre_list = []

        for idx, genre in enumerate(raw_genre_list):
            genre_list.append(Genre(genre, idx))

        return genre_list
