import numpy as np

class Genre:

    def __init__(self,
                 genre_name: str,
                 embedding: np.ndarray
                 ):
        self.name = genre_name
        self.embedding = embedding

    def to_dict(self):
        return {
            "genre_name": self.name,
            "embedding": self.embedding
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            genre_name=data['genre_name'],
            embedding=data['embedding']
        )
