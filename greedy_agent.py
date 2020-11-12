from agent import Agent
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra

debug = False


class GreedyAgent(Agent):

    def __init__(self, aid):
        super().__init__(aid)
        self.greedy_path = []

    def act(self, observation):
        if self.terminated:  # If terminated, return no-op
            return ("noop",)
        if self.is_moving(observation):  # if traversing on edge, return no-op
            return ("noop",)
        if debug:
            print("current greedy path is {}".format(self.greedy_path))
        location = observation.locations[self.aid][1]
        if not self.greedy_path:
            if debug:
                print("this is considered an empty list")
            graph = observation.graph
            self.greedy_path = self.get_path(graph, location)
        elif debug:
            print("this is not considered an empty list")
        next_vertex = self.greedy_path[0]
        weight = observation.graph[location][next_vertex]['weight']
        action = ("move", location, next_vertex, weight)
        self.greedy_path = self.greedy_path[1:]
        return action

    def get_path(self, graph, source):
        mininum_length = None
        chosen_path = None
        for target in graph.nodes(data=True):
            if target[1]['value'] > 0:
                length, path = single_source_dijkstra(graph, source, target[0])
                if mininum_length is None or length < mininum_length:
                    mininum_length = length
                    chosen_path = path
        print("going to vertex {}".format(chosen_path[-1]))
        return chosen_path[1:]



