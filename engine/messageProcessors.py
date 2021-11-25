from abc import ABC, abstractmethod
from engine.messages import TagMessage, OpinionMessage
from engine.storages import TagStorage, OpinionStorage
from engine.messageSenders import MessageSender
from pickle import dumps


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

    async def process_tag_message(self, message: TagMessage) -> bytes:
        if not self._tag_storage.contains_tag(message):
            self._tag_storage.put_tag(message)
            self._opinion_storage.increment_opinion(message)
            await self._message_sender.send_message(message)
        return bytearray()

    def process_opinion_message(self, message: OpinionMessage) -> bytes:
        top_n = self._opinion_storage.get_top_n(message)

        tags_list = []
        for response in top_n:
            tags_list.append(self._tag_storage.get_tag(response.id, message))
        return dumps(tuple([top_n, tags_list]))

