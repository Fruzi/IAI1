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


def get_path(graph, location):
    g_values = {edge: MAX for edge in graph.nodes()}
    g_values[location] = 0
    f_values = {edge: MAX for edge in graph.nodes()}
    f_values[location] = 0
    predecessors = {edge: None for edge in graph.nodes()}
    found_goal = False
    h = graph[location]
    h = list(h.items())
    h = [(f, s['weight']) for f, s in h]
    _heapq.heapify(h)
    while not found_goal:
        smallest = _heapq.heappop(h)
        if is_goal(graph, smallest):
            return reconstruct_path(smallest, predecessors)
        else:
            expansion = graph[smallest]
            expansion = list(expansion.items())
            expansion = [(f, s['weight']) for f, s in expansion]
            for item in expansion:
                _heapq.heappush(h, item)


class AStarAgent(Agent):

    def __init__(self, aid):
        super().__init__(aid)
        self.curr_path = []

    def act(self, observation):
        if self.terminated:  # If terminated, return no-op
            return ("noop",)
        if self.is_moving(observation):  # if traversing on edge, return no-op
            return ("noop",)
        location = observation.locations[self.aid][1]
        if not self.curr_path:
            graph = observation.graph
            self.curr_path = get_path(graph, location)
        next_vertex = self.curr_path[0]
        weight = observation.graph[location][next_vertex]['weight']
        action = ("move", location, next_vertex, weight)
        self.curr_path = self.curr_path[1:]
        return action
