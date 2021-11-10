from abc import ABC, abstractmethod
from messages import TagMessage, OpinionMessage
from storages import TagStorage, OpinionStorage
from messageSenders import MessageSender


class MessageProcessor(ABC):

    @abstractmethod
    def process_tag_message(self, message: TagMessage) -> bytes:
        pass

    @abstractmethod
    def process_opinion_message(self, message: OpinionMessage) -> bytes:
        pass


class DefaultMessageProcessor(MessageProcessor):

    def __init__(self, tag_storage: TagStorage, opinion_storage: OpinionStorage, message_sender: MessageSender):
        self._tag_storage = tag_storage
        self._opinion_storage = opinion_storage
        self._message_sender = message_sender

    def process_tag_message(self, message: TagMessage) -> bytes:
        if not self._tag_storage.contains_tag(message):
            self._tag_storage.put_tag(message)
            self._opinion_storage.increment_opinion(message)
            self._message_sender.send_message(message)
        return bytearray()

    def process_opinion_message(self, message: OpinionMessage) -> bytes:
        pass

