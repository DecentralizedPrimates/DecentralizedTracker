from abc import ABC, abstractmethod
# from engine.messageProcessors import MessageProcessor


class Message(ABC):

    @abstractmethod
    def accept(self, processor):
        pass


class TagMessage(Message):

    def __init__(self, info_hash, attribute, value, time, salt):
        self.info_hash = info_hash
        self.attribute = attribute
        self.value = value
        self.time = time
        self.salt = salt

    def accept(self, processor):
        return processor.process_tag_message(self)


class OpinionMessage(Message):

    def __init__(self, attribute, value):
        self.attribute = attribute
        self.value = value

    def accept(self, processor):
        return processor.process_opinion_message(self)

