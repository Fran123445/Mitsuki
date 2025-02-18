import numpy as np


class Media:

    def __init__(self,
                 media_id: int,
                 media_title: str,
                 media_genres: np.ndarray,
                 media_tags: np.ndarray,
                 media_description: str,
                 media_embedding: np.ndarray
                 ):
        self.media_id = media_id
        self.media_title = media_title
        self.media_genres = media_genres
        self.media_tags = media_tags
        self.media_description = media_description
        self.media_embedding = media_embedding

    def to_dict(self):
        return {
            "media_id": self.media_id,
            "media_title": self.media_title,
            "media_genres": list(self.media_genres),
            "media_tags": list(self.media_tags),
            "media_description": self.media_description,
            "media_embedding": self.media_embedding.tolist()  # Convert numpy array to list so mongo doesn't cry rivers
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            media_id=data.get('media_id', None),
            media_title=data.get('media_title', None),
            media_genres=np.array(data.get('media_genres', [])),
            media_tags=np.array(data.get('media_tags', [])),
            media_description=data.get('media_description', None),
            media_embedding=np.array(data.get('media_embedding', []))
        )
