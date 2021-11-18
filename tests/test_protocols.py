from engine.node_response import NodeResponse
from engine.lazy_synchornization_decision_making import LazySynchornizationDecisionMaker
import unittest
from engine.messages import TagMessage, OpinionMessage
from mocks.mockStorages import MockTagStorage, MockOpinionStorage

class TestLazySynchornizationDecisionMaker(unittest.TestCase):
    def setUp(self):
        pass

    def test_processing_tag_message(self):
        pass

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
