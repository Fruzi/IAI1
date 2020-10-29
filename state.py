class State:

    def __init__(self, graph, locations, time=0):
        self.time = time
        self.graph = graph
        self.locations = locations

    def advance_time(self, time_units=1):
        self.time += time_units
