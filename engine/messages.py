from abc import ABC, abstractmethod
# from messageProcessors import MessageProcessor


class Message(ABC):
    pass
    # @abstractmethod
    # def accept(self, processor: MessageProcessor):
    #     pass


class TagMessage(Message):

    def __init__(self, info_hash, attribute, value, time, salt):
        self.info_hash = info_hash
        self.attribute = attribute
        self.value = value
        self.time = time
        self.salt = salt

    pass
    # def accept(self, processor: MessageProcessor):
    #     return processor.process_tag_message(self)


class OpinionMessage(Message):
    pass
    # def accept(self, processor: MessageProcessor):
    #     return processor.process_opinion_message(self)

