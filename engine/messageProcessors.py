from abc import ABC, abstractmethod
from messages import TagMessage, OpinionMessage, MessageProcessor
from storages import TagStorage, OpinionStorage
from messageSenders import MessageSender
from pickle import dumps
import asyncio

class DefaultMessageProcessor(MessageProcessor):

    def __init__(self, tag_storage: TagStorage, opinion_storage: OpinionStorage, message_sender: MessageSender):
        self._tag_storage = tag_storage
        self._opinion_storage = opinion_storage
        self._message_sender = message_sender

    def process_tag_message(self, message: TagMessage) -> bytes:
        if not self._tag_storage.contains_tag(message):
            self._tag_storage.put_tag(message)
            self._opinion_storage.increment_opinion(message)
            asyncio.create_task(self._message_sender.send_message(message))
        return bytes()

    def process_opinion_message(self, message: OpinionMessage) -> bytes:
        top_n = self._opinion_storage.get_top_n(message)

        tags_list = []
        for response in top_n:
            tags_list.append(self._tag_storage.get_tag(response.id, message))
        return dumps(tuple([top_n, tags_list]))

