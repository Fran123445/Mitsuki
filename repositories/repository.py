from pymongo import MongoClient


class Repository:
    def __init__(self, mongo_client: MongoClient, database_name: str, collection_name: str):
        self._collection = mongo_client[database_name][collection_name]

    def insert(self, document: dict):
        return self._collection.insert_one(document)

    def create(self, model):
        """Inserts the document into the collection. The model is expected to have a .to_dict() method."""
        return self.insert(model.to_dict())

    def create_many(self, model_list):
        documents = [model.to_dict() for model in model_list]
        return self._collection.insert_many(documents)

    def get(self, query: dict, model_class):
        """
        Finds a document by query and returns a model instance.
        The model_class is expected to have a .from_dict() class method.
        """
        document = self._collection.find_one(query)
        return model_class.from_dict(document) if document else None

    def get_total_amount(self):
        self._collection.count_documents({})