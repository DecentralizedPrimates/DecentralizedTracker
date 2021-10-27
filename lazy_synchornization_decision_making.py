from node_response import NodeResponse
import numpy as np

class LazySynchornizationDecisionMaking:

    def __init__(self, min_number_to_find_median=4):
        self.min_number_to_find_median = min_number_to_find_median

    def make_decision(self, nodes_responses: list):
        # nodes_responses is a list of lists of node_response, where first list is a list od nodes,
        # inner lists are nodes responses

        dict = {}

        for node_responses in nodes_responses:
            for response in node_responses:
                key = tuple([response.id, response.attribute_name, response.attribute_value])
                if key not in dict:
                    dict[key] = [response.votes]
                else:
                    dict[key].append(response.votes)

        answer = []

        for key, value in dict.items():
            if len(value) >= self.min_number_to_find_median:
                median = np.median(value)
                answer.append(NodeResponse(key[0], key[1], key[2], median))

        return answer



