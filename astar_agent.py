import _heapq

from agent import Agent

MAX = 10000


def reconstruct_path(goal, predecessors):
    ret = [goal]
    prev = predecessors[goal]
    while prev is not None:
        ret = [prev] + ret
        curr = prev
        prev = predecessors[curr]
    return ret[1:]


class AStarAgent(Agent):

    def __init__(self, aid, limit, heuristic=None):
        super().__init__(aid)
        self.curr_path = []
        self.heuristic = heuristic
        self.limit = limit

    def act(self, observation):
        if self.terminated:  # If terminated, return no-op
            return ("noop",)
        if self.is_moving(observation):  # if traversing on edge, return no-op
            return ("noop",)
        location = observation.locations[self.aid][1]
        if not self.curr_path:
            graph = observation.graph
            self.curr_path = self.get_path(graph, location)
        if self.curr_path == "terminate":
            return ("terminate",)
        next_vertex = self.curr_path[0]
        weight = observation.graph[location][next_vertex]['weight']
        action = ("move", location, next_vertex, weight)
        self.curr_path = self.curr_path[1:]
        return action

    def get_path(self, graph, location):
        g_values = {vertex: MAX for vertex in graph.nodes()}
        g_values[location] = 0
        f_values = g_values.copy()
        predecessors = {vertex: None for vertex in graph.nodes()}
        num_previously_visited = {vertex: 0 for vertex in graph.nodes()}
        h = list(f_values.items())
        h = [(f_value, vid) for vid, f_value in h]
        _heapq.heapify(h)
        num_expansions = 0
        while num_expansions < self.limit:
            smallest = _heapq.heappop(h)[1]
            if self.heuristic(graph, smallest, num_previously_visited[smallest]) == 0:
                return reconstruct_path(smallest, predecessors)
            else:
                num_expansions += 1
                expansion = graph[smallest]
                expansion = list(expansion.items())
                for neighbor in expansion:
                    new_possible_g = g_values[smallest] + neighbor[1]['weight']
                    if new_possible_g < g_values[neighbor[0]]:
                        num_previously_visited[neighbor] = num_previously_visited[smallest]
                        if graph.nodes(data=True)[smallest] > 0:
                            num_previously_visited[neighbor] += 1
                        neighbor_id = neighbor[0]
                        g_values[neighbor_id] = new_possible_g
                        predecessors[neighbor_id] = smallest
                        f_values[neighbor_id] = new_possible_g + \
                                                self.heuristic(graph, neighbor, num_previously_visited[neighbor_id])
                        if neighbor_id not in h:
                            _heapq.heappush(h, (f_values[neighbor[0]], neighbor[0]))
        return "terminate"
