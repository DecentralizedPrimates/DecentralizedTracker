from __future__ import annotations
from abc import ABC, abstractmethod


class Message(ABC):

    @abstractmethod
    def accept(self, processor: MessageProcessor):
        pass


class TagMessage(Message):

    def __init__(self, info_hash, attribute, value, time, salt):
        self.info_hash = info_hash
        self.attribute = attribute
        self.value = value
        self.time = time
        self.salt = salt

    def accept(self, processor: MessageProcessor):
        return processor.process_tag_message(self)


class OpinionMessage(Message):

    def __init__(self, attribute, value):
        self.attribute = attribute
        self.value = value

    def accept(self, processor: MessageProcessor):
        return processor.process_opinion_message(self)


class MessageProcessor(ABC):

    @abstractmethod
    def process_tag_message(self, message: TagMessage) -> bytes:
        pass

    @abstractmethod
    def process_opinion_message(self, message: OpinionMessage) -> bytes:
        pass

