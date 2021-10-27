from node_response import NodeResponse
from lazy_synchornization_decision_making import LazySynchornizationDecisionMaking

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

lsmd = LazySynchornizationDecisionMaking()

ans = lsmd.make_decision(test_list)
for a in ans:
    print(a)
