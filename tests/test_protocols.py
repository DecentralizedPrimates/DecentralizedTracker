from engine.node_response import NodeResponse
from engine.lazy_synchornization_decision_making import LazySynchornizationDecisionMaker
from engine.messageHandlers import DefaultMessageHandler
from engine.messageProcessors import DefaultMessageProcessor
from engine.messageSenders import DefaultMessageSender

import unittest
from engine.messages import TagMessage, OpinionMessage
from mocks.mockStorages import MockTagStorage, MockOpinionStorage
from kademlia.network import Server
import asyncio

import threading

class TestLazySynchornizationDecisionMaker(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bootstrap_node = ("localhost", 8470)

    # def test_t(self):
    #     asyncio.run(self._server())

    async def f1(self):
        server = Server()
        tag_storage = MockTagStorage()
        opinion_storage = MockOpinionStorage()
        messageSender = DefaultMessageSender(server)
        messageHandler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, messageSender))
        messageProcessor = DefaultMessageProcessor(tag_storage, opinion_storage, messageSender)
        await server.listen(8470, messageHandler)

    async def f2(self):
        server1 = Server()
        tag_storage1 = MockTagStorage()
        opinion_storage1 = MockOpinionStorage()
        messageSender1 = DefaultMessageSender(server1)
        messageHandler1 = DefaultMessageHandler(DefaultMessageProcessor(tag_storage1, opinion_storage1, messageSender1))
        await server1.listen(8471, messageHandler1)
        await server1.bootstrap([self.bootstrap_node])

    def _server(self):
        asyncio.run(self.f1())

        # tag1 = TagMessage('1', 'genre', 'comedy', 100.0, '0')
        # await messageProcessor.process_tag_message(tag1)

    def _server_1(self):
        asyncio.run(self.f2())


    async def test_processing_tag_message(self):
        threading.Thread(target=self._server).start()
        threading.Thread(target=self._server_1).start()
        # server2 = Server()
        # tag_storage2 = MockTagStorage()
        # opinion_storage2 = MockOpinionStorage()
        # messageSender2 = DefaultMessageSender(server2)
        # messageHandler2 = DefaultMessageHandler(DefaultMessageProcessor(tag_storage2, opinion_storage2, messageSender2))
        # await server2.listen(8472, messageHandler2)
        # await server2.bootstrap([bootstrap_node])


        # self.assertTrue(tag_storage.contains_tag(tag1))
        # self.assertTrue(tag_storage1.contains_tag(tag1))
        # self.assertTrue(tag_storage2.contains_tag(tag1))

        # key = (tag1.info_hash, tag1.attribute, tag1.value)

        # self.assertTrue(opinion_storage._opinions[key] == 1)
        # self.assertTrue(opinion_storage1._opinions[key] == 1)
        # self.assertTrue(opinion_storage2._opinions[key] == 1)

        # server.stop()
        # server1.stop()
        # server2.stop()

    # def test_processing_opinion_message(self):
    #     pass
    #
    # def test_tag_storage(self):
    #     tag_storage = MockTagStorage()
    #     tag1 = TagMessage('1', 'genre', 'comedy', 100.0, '0')
    #     tag2 = TagMessage('2', 'genre', 'comedy', 101.0, '0')
    #     tag_storage.put_tag(tag1)
    #     self.assertTrue(tag_storage.contains_tag(tag1))
    #     self.assertFalse(tag_storage.contains_tag(tag2))

if __name__ == "__main__":
  unittest.main()
