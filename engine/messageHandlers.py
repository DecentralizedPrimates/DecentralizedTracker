from kademlia.handlers import MessageHandler
from pickle import loads
from engine.messages import Message
from engine.messageProcessors import MessageProcessor


class DefaultMessageHandler(MessageHandler):

    def __init__(self, processor: MessageProcessor):
        self.processor = processor

    def notify(self, message: bytes) -> bytes:
        m: Message = loads(message)
        return m.accept(self.processor)

