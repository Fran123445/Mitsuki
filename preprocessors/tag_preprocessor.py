from sentence_transformers import SentenceTransformer

from models.tag import Tag


class TagPreprocessor:

    def __init__(self, sentence_transformer: SentenceTransformer):
        self.sentence_transformer = sentence_transformer

    def preprocess(self, raw_tag_list: list[dict]):
        tag_list = []

        for idx, tag in enumerate(raw_tag_list):
            embedding = self.sentence_transformer.encode(tag["name"])
            tag_list.append(Tag(tag["id"], tag["name"], embedding, idx))

        return tag_list
