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
        self._info = dict()

    def increment_opinion(self, tag: TagMessage):
        key = (tag.attribute, tag.value)
        if key not in self._opinions:
            self._opinions[key] = 0
        self._opinions[key] += 1

        if tag.info_hash not in self._info:
            self._info[tag.info_hash] = dict()
        if tag.attribute not in self._info[tag.info_hash]:
            self._info[tag.info_hash][tag.attribute] = dict()




    def get_top_n(self, message: OpinionMessage):
        pass

    # def get_info(self, info_hash):
