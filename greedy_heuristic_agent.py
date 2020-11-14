from agent import Agent
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra


class GreedyHeuristicAgent(Agent):

    def __init__(self, aid, limit):
        super().__init__(aid)
        self.limit = limit

    def act(self, observation):
        if self.terminated:  # If terminated, return no-op
            return ("noop",)
        if self.is_moving(observation):  # if traversing on edge, return no-op
            return ("noop",)
        location = observation.locations[self.aid][1]
        next_vertex = self.get_greedy_move(observation.graph, location)
        weight = observation.graph[location][next_vertex]['weight']
        action = ("move", location, next_vertex, weight)
        return action

    def get_greedy_move(self, graph, location):
        next_vertex = None
        cheapest = None
        for neighbor in graph[location]:
            if graph.nodes(data=True)[neighbor]['value'] > 0 and\
                    (cheapest is None or graph[location][neighbor]['weight'] < cheapest):
                next_vertex = neighbor
                cheapest = graph[location][neighbor]['weight']
        if next_vertex is None:
            for neighbor in graph[location]:
                if cheapest is None or graph[location][neighbor]['weight'] < cheapest:
                    next_vertex = neighbor[0]
                    cheapest = neighbor[1]['weight']
        return next_vertex



