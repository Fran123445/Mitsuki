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
