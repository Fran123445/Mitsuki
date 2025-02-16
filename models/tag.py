import numpy as np


class Tag:

    def __init__(self,
                 tag_id: int,
                 tag_name: str,
                 tag_embedding: np.ndarray,
                 tag_index: int
                 ):
        self.id = tag_id
        self.name = tag_name
        self.embedding = tag_embedding
        self.index = tag_index

    def to_dict(self):
        return {
            "tag_id": self.id,
            "tag_name": self.name,
            "tag_embedding": self.embedding.tolist(),  # Convert numpy array to list so mongo doesn't cry
            "tag_index": self.index
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            tag_id=data['tag_id'],
            tag_name=data['tag_name'],
            tag_embedding=np.array(data['tag_embedding']),
            tag_index=data['tag_index']
        )
