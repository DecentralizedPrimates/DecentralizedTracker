import pickle
from abc import ABC, abstractmethod
from engine.messages import Message
from kademlia.network import Server


class MessageSender(ABC):

    @abstractmethod
    async def send_message(self, message: Message) -> bytes:
        pass


class DefaultMessageSender(MessageSender):

    _instance = None

    def __init__(self, server: Server):
        self._server = server

    async def send_message(self, message: Message):
        b: bytes = pickle.dumps(message)
        return await self._server.query(b)