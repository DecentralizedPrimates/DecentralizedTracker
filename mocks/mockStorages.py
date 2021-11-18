from engine.messages import TagMessage, OpinionMessage
from engine.storages import TagStorage, OpinionStorage


class MockTagStorage(TagStorage):

    def __init__(self):
        self._tags = set()

    def contains_tag(self, tag: TagMessage) -> bool:
        return tag in self._tags

    def put_tag(self, tag: TagMessage):
        self._tags.add(tag)

    def get_tag(self, info_hash, message: OpinionMessage) -> TagMessage:
        pass


class MockOpinionStorage(OpinionStorage):

    def __init__(self):
        self._opinions = dict()

    def increment_opinion(self, tag: TagMessage):
        key = (tag.info_hash, tag.attribute, tag.value)
        if key not in self._opinions:
            self._opinions[key] = 0
        self._opinions[key] += 1

    def get_top_n(self, message: OpinionMessage):
        pass
