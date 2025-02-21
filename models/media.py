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
                 season_year: int
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
        self.season_year = season_year

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
            "season_year": self.season_year
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
            season_year=data.get('season_year', None)
        )
