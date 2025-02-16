import numpy as np


class Media:

    def __init__(self,
                 media_id: int,
                 media_title: str,
                 media_genres: list[int],
                 media_tags: list[int],
                 media_description: str,
                 media_embedding: np.ndarray
                 ):
        self.media_id = media_id
        self.media_title = media_title
        self.media_genres = media_genres
        self.media_tags = media_tags
        self.media_description = media_description
        self.media_embedding = media_embedding
