import numpy as np


class Media:

    def __init__(self,
                 id: int,
                 id_mal: int,
                 title_romaji: str,
                 title_english: str,
                 genres: set,
                 tags: dict,
                 description: str,
                 tag_embedding: np.ndarray,
                 genre_embedding: np.ndarray,
                 image_url: str,
                 year: int,
                 mean_score: int,
                 popularity: int,
                 is_adult: bool,
                 format: str,
                 ):
        self.id = id
        self.id_mal = id_mal
        self.title_romaji = title_romaji
        self.title_english = title_english
        self.genres = genres
        self.tags = tags
        self.descriptions = description
        self.tag_embedding = tag_embedding
        self.genre_embedding = genre_embedding
        self.image_url = image_url
        self.year = year
        self.mean_score = mean_score
        self.popularity = popularity
        self.is_adult = is_adult
        self.format = format

    def to_dict(self):
        return {
            "id": self.id,
            "id_mal": self.id_mal,
            "title_romaji": self.title_romaji,
            "title_english": self.title_english,
            "genres": list(self.genres),
            "tags": self.tags,
            "description": self.descriptions,
            "tag_embedding": self.tag_embedding.tolist(),  # Convert numpy array to list so mongo doesn't cry rivers
            "genre_embedding": self.genre_embedding.tolist(),
            "image_url": self.image_url,
            "year": self.year,
            "mean_score": self.mean_score,
            "popularity": self.popularity,
            "is_adult": self.is_adult,
            "format": self.format
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            id=data.get('id', None),
            id_mal=data.get('id_mal', None),
            title_romaji=data.get('title_romaji', None),
            title_english=data.get('title_english', None),
            genres=data.get('genres', set()),
            tags=data.get('tags', {}),
            description=data.get('description', None),
            tag_embedding=np.array(data.get('tag_embedding', [])),
            genre_embedding=np.array(data.get('genre_embedding', [])),
            image_url=data.get('image_url', None),
            year=data.get('year', None),
            mean_score=data.get('mean_score', None),
            popularity=data.get('popularity', None),
            is_adult=data.get('is_adult', None),
            format=data.get('format', None)
        )
