

class Genre:

    def __init__(self,
                 genre_name: str,
                 genre_index: int
                 ):
        self.name = genre_name
        self.index = genre_index

    def to_dict(self):
        return {
            "genre_name": self.name,
            "genre_index": self.index
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            genre_name=data['genre_name'],
            genre_index=data['genre_index']
        )
