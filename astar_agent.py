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
        f_values = {vertex: MAX for vertex in graph.nodes()}
        f_values[location] = self.heuristic(graph, location, 0)
        added_to_h = {vertex: False for vertex in graph.nodes()}
        added_to_h[location] = True
        predecessors = {vertex: None for vertex in graph.nodes()}
        num_previously_visited = {vertex: 0 for vertex in graph.nodes()}
        h = [(self.heuristic(graph, location, num_previously_visited[location]), location)]
        _heapq.heapify(h)
        num_expansions = 0
        while num_expansions < self.limit:
            if not h:
                print(f_values)
            print(h)
            smallest = _heapq.heappop(h)
            smallest = smallest[1]
            added_to_h[smallest] = False
            print("heuristic value of vertex {} is {}".format(smallest, self.heuristic(graph, smallest, num_previously_visited[smallest])))
            if self.heuristic(graph, smallest, num_previously_visited[smallest]) == 0:
                return reconstruct_path(smallest, predecessors)
            else:
                num_expansions += 1
                expansion = graph[smallest]
                expansion = list(expansion.items())
                for neighbor in expansion:
                    neighbor_id = neighbor[0]
                    new_possible_g = g_values[smallest] + neighbor[1]['weight']
                    if new_possible_g < g_values[neighbor_id]:
                        num_previously_visited[neighbor_id] = num_previously_visited[smallest]
                        if graph.nodes(data=True)[smallest]['value'] > 0:
                            num_previously_visited[neighbor_id] += 1
                        g_values[neighbor_id] = new_possible_g
                        predecessors[neighbor_id] = smallest
                        f_values[neighbor_id] = new_possible_g + \
                                                self.heuristic(graph, neighbor, num_previously_visited[neighbor_id])
                        if not added_to_h[neighbor_id]:
                            _heapq.heappush(h, (f_values[neighbor[0]], neighbor[0]))
                            added_to_h[neighbor_id] = True

        return "terminate"
