
class UserMediaRecommendations:

    def __init__(self,
                 id: int,
                 recommendations: dict[int, int],
                 ):
        self.id = id
        self.recommendations = recommendations

    def to_dict(self):
        return {
            "id": self.id,
            "recommendations": {str(k): v for k, v in self.recommendations.items()}
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            id=data['id'],
            recommendations={int(k):v for k,v in data['recommendations'].items()}
        )