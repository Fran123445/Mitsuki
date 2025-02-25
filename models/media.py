import numpy as np


class Media:

    def __init__(self,
                 media_id: int,
                 media_id_mal: int,
                 media_title_romaji: str,
                 media_title_english: str,
                 media_genres: np.ndarray,
                 media_tags: np.ndarray,
                 media_description: str,
                 media_embedding: np.ndarray,
                 image_url: str,
                 year: int,
                 average_score: int,
                 popularity: int,
                 is_adult: bool
                 ):
        self.media_id = media_id
        self.media_id_mal = media_id_mal
        self.media_title_romaji = media_title_romaji
        self.media_title_english = media_title_english
        self.media_genres = media_genres
        self.media_tags = media_tags
        self.media_description = media_description
        self.media_embedding = media_embedding
        self.image_url = image_url
        self.year = year
        self.average_score = average_score
        self.popularity = popularity
        self.is_adult = is_adult

    def to_dict(self):
        return {
            "media_id": self.media_id,
            "media_id_mal": self.media_id_mal,
            "media_title_romaji": self.media_title_romaji,
            "media_title_english": self.media_title_english,
            "media_genres": list(self.media_genres),
            "media_tags": list(self.media_tags),
            "media_description": self.media_description,
            "media_embedding": self.media_embedding.tolist(),  # Convert numpy array to list so mongo doesn't cry rivers
            "image_url": self.image_url,
            "year": self.year,
            "average_score": self.average_score,
            "popularity": self.popularity,
            "is_adult": self.is_adult
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            media_id=data.get('media_id', None),
            media_id_mal=data.get('media_id_mal', None),
            media_title_romaji=data.get('media_title_romaji', None),
            media_title_english=data.get('media_title_english', None),
            media_genres=np.array(data.get('media_genres', [])),
            media_tags=np.array(data.get('media_tags', [])),
            media_description=data.get('media_description', None),
            media_embedding=np.array(data.get('media_embedding', [])),
            image_url=data.get('image_url', None),
            year=data.get('year', None),
            average_score=data.get('average_score', None),
            popularity=data.get('popularity', None),
            is_adult=data.get('is_adult', None)
        )
