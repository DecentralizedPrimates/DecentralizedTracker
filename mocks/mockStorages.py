from engine.messages import TagMessage, OpinionMessage
from engine.storages import TagStorage, OpinionStorage
from engine.node_response import NodeResponse

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
        key = (tag.attribute, tag.value)
        if key not in self._opinions:
            self._opinions[key] = dict()
        if tag.info_hash not in self._opinions[key]:
            self._opinions[key][tag.info_hash] = 0
        self._opinions[key][tag.info_hash] += 1

        if tag.info_hash not in self._info:
            self._info[tag.info_hash] = dict()
        if tag.attribute not in self._info[tag.info_hash]:
            self._info[tag.info_hash][tag.attribute] = dict()

     def get_top_n(self, message: OpinionMessage, n=10):
        key = (message.attribute, message.value)

        dict_list = [(k, v) for k, v in self._opinions[key].items()]
        dict_list.sort(key=lambda x: x[1])

        top_n = []
        for i in range(len(dict_list)):
            if len(top_n) >= 10:
                break
            top_n.append(NodeResponse(dict_list[i][0], message.attribute, message.value, dict_list[i][1]))
        return top_n