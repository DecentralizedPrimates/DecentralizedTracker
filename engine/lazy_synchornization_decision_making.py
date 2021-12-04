from engine.node_response import NodeResponse
import numpy as np


class LazySynchronizationDecisionMaker:

    def __init__(self, min_number_to_find_median=4):
        self._min_number_to_find_median = min_number_to_find_median

    def make_decision(self, nodes_responses: list):
        # nodes_responses is a list of lists of node_response, where first list is a list of nodes,
        # inner lists are nodes responses

        votes = {}

        for node_responses in nodes_responses:
            for response in node_responses:
                key = tuple([response.id, response.attribute_name, response.attribute_value])
                if key not in votes:
                    votes[key] = []
                votes[key].append(response.votes)

        answer = []

        for key, value in votes.items():
            if len(value) >= self._min_number_to_find_median:
                median = int(np.median(value))
                answer.append(NodeResponse(key[0], key[1], key[2], median))

        return answer



