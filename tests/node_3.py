from engine.messageHandlers import DefaultMessageHandler
from engine.messageProcessors import DefaultMessageProcessor
from engine.messageSenders import DefaultMessageSender

from engine.messages import TagMessage, OpinionMessage
from mocks.mockStorages import MockTagStorage, MockOpinionStorage
import logging
import asyncio

from kademlia.network import Server

async def run():
    server = Server()
    opinion_storage = MockOpinionStorage()
    tag_storage = MockTagStorage()
    messageSender = DefaultMessageSender(server)
    messageHandler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, messageSender))

    await server.listen(8471, messageHandler)
    bootstrap_node = ("localhost", 8470)
    await server.bootstrap([bootstrap_node])
    tag1 = TagMessage('1', 'genre', 'comedy', 100.0, '0')
    result = await messageSender.send_message(tag1)
    print("Get result:", result)
    # server.stop()

asyncio.run(run())