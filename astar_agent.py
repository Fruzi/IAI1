import _heapq

from agent import Agent

MAX = 10000

def is_goal(graph, location):
    return graph.nodes(data=True)[location][1]['value'] > 0


def reconstruct_path(goal, predecessors):
    ret = list(goal)
    prev = predecessors[goal]
    while prev is not None:
        ret = list(prev) + ret
        curr = prev
        prev = predecessors[curr]
    return ret


def get_path(graph, location, heuristic):
    g_values = {edge: MAX for edge in graph.nodes()}
    g_values[location] = 0
    f_values = g_values.copy()
    predecessors = {edge: None for edge in graph.nodes()}
    h = list(f_values.items())
    _heapq.heapify(h)
    while True:
        smallest = _heapq.heappop(h)
        if is_goal(graph, smallest):
            return reconstruct_path(smallest, predecessors)
        else:
            expansion = graph[smallest]
            expansion = list(expansion.items())
            for neighbor in expansion:
                new_possible_g = g_values[smallest] + neighbor[1]['weight']
                if new_possible_g < g_values[neighbor[0]]:
                    neighbor_id = neighbor[0]
                    g_values[neighbor_id] = new_possible_g
                    predecessors[neighbor_id] = smallest[0]
                    f_values[neighbor_id] = new_possible_g + heuristic[neighbor]
                    # TODO might not work as intended
                    if neighbor_id not in h:
                        _heapq.heappush(h, (neighbor[0], f_values[neighbor[0]]))


class AStarAgent(Agent):

    def __init__(self, aid, heuristic=None):
        super().__init__(aid)
        self.curr_path = []
        self.heuristic = heuristic

    def act(self, observation):
        if self.terminated:  # If terminated, return no-op
            return ("noop",)
        if self.is_moving(observation):  # if traversing on edge, return no-op
            return ("noop",)
        location = observation.locations[self.aid][1]
        if not self.curr_path:
            graph = observation.graph
            # TODO probably need to remove first vetex in path, easy fix but check
            self.curr_path = get_path(graph, location, self.heuristic)
        next_vertex = self.curr_path[0]
        weight = observation.graph[location][next_vertex]['weight']
        action = ("move", location, next_vertex, weight)
        self.curr_path = self.curr_path[1:]
        return action
