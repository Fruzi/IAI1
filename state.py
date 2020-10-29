class State:

    def __init__(self, graph, locations, time=0):
        self.time = time
        self.graph = graph
        self.locations = locations
        self.people_remaining = sum(node[1]['value'] for node in graph.nodes.data())

    def advance_time(self, time_units=1):
        self.time += time_units
