from abc import ABC, abstractmethod
from messages import TagMessage, OpinionMessage


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
    def get_top_n(self, message: OpinionMessage):
        pass
