from abc import ABC, abstractmethod
from messages import TagMessage, OpinionMessage

tag_dict = {}
opinion_dict = {}


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

    @abstractmethod
    def dict_contains_tag(self, tag: TagMessage) -> bool:
        pass

    @abstractmethod
    def dict_put_tag(self, tag: TagMessage):
        pass

    @abstractmethod
    def dict_get_tag(self, info_hash, message: OpinionMessage) -> TagMessage:
        pass

class OpinionStorage(ABC):

    @abstractmethod
    def increment_opinion(self, tag: TagMessage):
        pass

    @abstractmethod
    def get_top_n(self, message: OpinionMessage):  # return list of NodeResponse
        pass

    @abstractmethod
    def dict_increment_opinion(self, tag: TagMessage):
        pass

    @abstractmethod
    def dict_get_top_n(self, message: OpinionMessage):  # return list of NodeResponse
        pass