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

class TestLazySynchornizationDecisionMaker(unittest.TestCase):
    def setUp(self):
        pass

    def test_t(self):
        asyncio.run(self._processing_tag_message())

    async def _processing_tag_message(self):
        server = Server()
        tag_storage = MockTagStorage()
        opinion_storage = MockOpinionStorage()
        messageSender = DefaultMessageSender(server)
        messageHandler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, messageSender))
        messageProcessor = DefaultMessageProcessor(tag_storage, opinion_storage, messageSender)
        await server.listen(8470, messageHandler)
        bootstrap_node = ("localhost", 8470)

        # server1 = Server()
        # tag_storage1 = MockTagStorage()
        # opinion_storage1 = MockOpinionStorage()
        # messageSender1 = DefaultMessageSender(server1)
        # messageHandler1 = DefaultMessageHandler(DefaultMessageProcessor(tag_storage1, opinion_storage1, messageSender1))
        # await server1.listen(8471, messageHandler1)
        # await server1.bootstrap([bootstrap_node])

        # server2 = Server()
        # tag_storage2 = MockTagStorage()
        # opinion_storage2 = MockOpinionStorage()
        # messageSender2 = DefaultMessageSender(server2)
        # messageHandler2 = DefaultMessageHandler(DefaultMessageProcessor(tag_storage2, opinion_storage2, messageSender2))
        # await server2.listen(8472, messageHandler2)
        # await server2.bootstrap([bootstrap_node])
        #
        tag1 = TagMessage('1', 'genre', 'comedy', 100.0, '0')
        await messageProcessor.process_tag_message(tag1)

        self.assertTrue(tag_storage.contains_tag(tag1))
        # self.assertTrue(tag_storage1.contains_tag(tag1))
        # self.assertTrue(tag_storage2.contains_tag(tag1))

        key = (tag1.info_hash, tag1.attribute, tag1.value)

        self.assertTrue(opinion_storage._opinions[key] == 1)
        # self.assertTrue(opinion_storage1._opinions[key] == 1)
        # self.assertTrue(opinion_storage2._opinions[key] == 1)

        server.stop()
        # server1.stop()
        # server2.stop()

    def test_processing_opinion_message(self):
        pass

    def test_tag_storage(self):
        tag_storage = MockTagStorage()
        tag1 = TagMessage('1', 'genre', 'comedy', 100.0, '0')
        tag2 = TagMessage('2', 'genre', 'comedy', 101.0, '0')
        tag_storage.put_tag(tag1)
        self.assertTrue(tag_storage.contains_tag(tag1))
        self.assertFalse(tag_storage.contains_tag(tag2))

if __name__ == "__main__":
  unittest.main()
