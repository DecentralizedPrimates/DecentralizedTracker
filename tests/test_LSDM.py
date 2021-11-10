from engine.node_response import NodeResponse
from engine.lazy_synchornization_decision_making import LazySynchornizationDecisionMaker
import unittest


class TestLazySynchornizationDecisionMaker(unittest.TestCase):
    def setUp(self):
        self.lsmd = LazySynchornizationDecisionMaker()

    def test_lsmd(self):
        test_list = []

        node1 = []
        node2 = []
        node3 = []
        node4 = []
        node5 = []

        node1.append(NodeResponse("1", "genre", "comedy", 10))
        node2.append(NodeResponse("1", "genre", "comedy", 15))
        node3.append(NodeResponse("1", "genre", "comedy", 12))
        node4.append(NodeResponse("1", "genre", "comedy", 13))
        node4.append(NodeResponse("1", "genre", "comedy", 1))

        node1.append(NodeResponse("2", "genre", "drama", 2))
        node3.append(NodeResponse("2", "genre", "drama", 5))
        node5.append(NodeResponse("2", "genre", "drama", 7))

        node1.append(NodeResponse("1", "artist", "Den", 7))
        node2.append(NodeResponse("1", "artist", "Den", 20))
        node4.append(NodeResponse("1", "artist", "Den", 56))
        node5.append(NodeResponse("1", "artist", "Den", 14))

        node1.append(NodeResponse("3", "artist", "Rob", 15))
        node3.append(NodeResponse("3", "artist", "Rob", 4))

        test_list.append(node1)
        test_list.append(node2)
        test_list.append(node3)
        test_list.append(node4)
        test_list.append(node5)

        ans = self.lsmd.make_decision(test_list)

        self.assertEqual(len(ans), 2)

        self.assertEqual(ans[0].id, '1')
        self.assertEqual(ans[0].attribute_name, 'genre')
        self.assertEqual(ans[0].attribute_value, 'comedy')
        self.assertEqual(ans[0].votes, 12)

        self.assertEqual(ans[1].id, '1')
        self.assertEqual(ans[1].attribute_name, 'artist')
        self.assertEqual(ans[1].attribute_value, 'Den')
        self.assertEqual(ans[1].votes, 17)


if __name__ == "__main__":
  unittest.main()
