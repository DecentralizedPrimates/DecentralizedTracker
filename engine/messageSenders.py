import pickle
from abc import ABC, abstractmethod
from engine.messages import Message
from kademlia.network import Server


class MessageSender(ABC):

    @abstractmethod
    async def send_message(self, message: Message) -> bytes:
        pass


class DefaultMessageSender(MessageSender):

    def __init__(self, server: Server):
        self._server = server

    def send_message(self, message: Message):
        b: bytes = pickle.dumps(message)
        print(b)
        return self._server.query(b)

