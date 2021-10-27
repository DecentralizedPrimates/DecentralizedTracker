class NodeResponse:
    def __init__(self, id, attribute_name, attribute_value, votes):
        self.id = id
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.votes = votes

    def __str__(self):
        print("id =", self.id)
        print("attribute_name =", self.attribute_name)
        print("attribute_value =", self.attribute_value)
        print("votes =", self.votes)
        return ""