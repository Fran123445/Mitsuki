from sentence_transformers import SentenceTransformer

from models.tag import Tag


class TagPreprocessor:

    def __init__(self, sentence_transformer: SentenceTransformer):
        self.sentence_transformer = sentence_transformer

    def preprocess(self, raw_tag_list: list[dict]):
        tag_list = []

        for tag in raw_tag_list:
            embedding = self.sentence_transformer.encode(tag["name"])
            tag_list.append(Tag(tag["id"], tag["name"], embedding))

        return tag_list
