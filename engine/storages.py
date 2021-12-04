from abc import ABC, abstractmethod
from engine.messages import TagMessage, OpinionMessage
from queryEntities import InfoQuery, OpinionMessageQuery


class TagStorage(ABC):

    @abstractmethod
    def contains_tag(self, tag: TagMessage) -> bool:
        pass

    @abstractmethod
    def put_tag(self, tag: TagMessage):
        pass

    @abstractmethod
    def get_tag(self, info_hash, message: OpinionMessage) -> TagMessage:
        pass


class OpinionStorage(ABC):

    @abstractmethod
    def increment_opinion(self, tag: TagMessage):
        pass

    @abstractmethod
    def get_top_n(self, message: OpinionMessageQuery):  # return list of NodeResponse
        pass

    @abstractmethod
    def get_title(self, info_query: InfoQuery):
        pass

    @abstractmethod
    def get_top_n_attributes(self, info_query: InfoQuery, n: int):
        pass
