from engine.messages import TagMessage, OpinionMessage
from engine.storages import TagStorage, OpinionStorage
from engine.node_response import NodeResponse
from engine.queryEntities import InfoQuery, OpinionMessageQuery


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
            self._opinions[key] = dict()
        if tag.info_hash not in self._opinions[key]:
            self._opinions[key][tag.info_hash] = 0
        self._opinions[key][tag.info_hash] += 1

        if tag.info_hash not in self._info:
            self._info[tag.info_hash] = dict()
        if tag.attribute not in self._info[tag.info_hash]:
            self._info[tag.info_hash][tag.attribute] = dict()
        if tag.value not in self._info[tag.info_hash][tag.attribute]:
            self._info[tag.info_hash][tag.attribute][tag.value] = 0
        self._info[tag.info_hash][tag.attribute][tag.value] += 1

    def get_title(self, info_hash: str):
        try:
            titles = [(title, votes) for title, votes in self._info[info_hash]['title'].items()]
            titles.sort(key=lambda x: x[1], reverse=True)
            return titles[0][0]
        except:
            return "Unknown Title"

    def get_top_n_attributes(self, info_hash: str, n=5):
        try:
            tags = []
            for attribute, values in self._info[info_hash].items():
                if attribute != 'title':
                    for attribute_value, votes in values.items():
                        tags.append((attribute, attribute_value, votes))
            tags.sort(key=lambda x: x[2], reverse=True)
            tags = tags[:n]
            return [(tag[0], tag[1]) for tag in tags]
        except:
            return []

    def get_top_n(self, message: OpinionMessageQuery, n=10):
        key = (message.attribute, message.value)

        dict_list = [(k, v) for k, v in self._opinions[key].items()]
        dict_list.sort(key=lambda x: x[1])

        top_n = []
        for i in range(len(dict_list)):
            if len(top_n) >= n:
                break
            top_n.append(NodeResponse(dict_list[i][0], message.attribute, message.value, dict_list[i][1]))
        return top_n
