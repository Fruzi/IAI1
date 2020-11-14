
import _heapq
from agent import Agent

MAX = 10000


def reconstruct_path(goal, predecessors):
    location = goal[1]
    ret = [location]
    while True:
        if goal in predecessors:
            pred = predecessors[goal]
            ret = [pred[1]] + ret
            goal = pred
        else:
            break
    return ret[1:]


def is_goal(graph_and_loc):
    graph = graph_and_loc[0]
    loc = graph_and_loc[1]
    for v in graph.nodes(data=True):
        if v[0] != loc and v[1]['value'] > 0:
            return False
    return True


def create_new_graph(graph, new_loc):
    g = graph.copy()
    g.add_node(new_loc, value=0)
    return g


class AStarAgent2(Agent):

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
        graph_and_loc_next_id = 0
        graph_and_loc_to_ids = {}
        ids_to_graph_and_loc = {}
        g_values = {(graph, location): 0}
        f_values = {(graph, location): self.heuristic(graph, location)}
        predecessors = {}
        graph_and_loc_to_ids[(graph, location)] = graph_and_loc_next_id
        ids_to_graph_and_loc[graph_and_loc_next_id] = (graph, location)
        graph_and_loc_next_id += 1
        h = [(self.heuristic(graph, location), graph_and_loc_to_ids[(graph, location)])]
        _heapq.heapify(h)
        added_to_h = [(graph, location)]
        num_expansions = 0
        while num_expansions < self.limit:
            popped_heuristic_value, popped_graph_and_loc = _heapq.heappop(h)
            popped_graph_and_loc = ids_to_graph_and_loc[popped_graph_and_loc]
            added_to_h.remove(popped_graph_and_loc)
            if is_goal(popped_graph_and_loc):
                return reconstruct_path(popped_graph_and_loc, predecessors)
            else:
                num_expansions += 1
                # all neighbors from current loc
                expansion = graph[popped_graph_and_loc[1]]
                expansion = list(expansion.items())
                for neighbor in expansion:
                    neighbor_id = neighbor[0]
                    neighbor_weight = neighbor[1]['weight']
                    new_possible_g = g_values[popped_graph_and_loc] + neighbor_weight
                    g = create_new_graph(popped_graph_and_loc[0], neighbor_id)
                    new_graph_and_loc = (g, neighbor_id)
                    if new_graph_and_loc not in g_values or new_possible_g < g_values[new_graph_and_loc]:
                        g_values[new_graph_and_loc] = new_possible_g
                        predecessors[new_graph_and_loc] = popped_graph_and_loc
                        f_values[new_graph_and_loc] = new_possible_g + \
                                                self.heuristic(new_graph_and_loc[0], new_graph_and_loc[1])
                        if new_graph_and_loc not in added_to_h:
                            graph_and_loc_to_ids[new_graph_and_loc] = graph_and_loc_next_id
                            ids_to_graph_and_loc[graph_and_loc_next_id] = new_graph_and_loc
                            graph_and_loc_next_id += 1
                            _heapq.heappush(h, (f_values[new_graph_and_loc], graph_and_loc_to_ids[new_graph_and_loc]))
                            added_to_h.append(new_graph_and_loc)
        return "terminate"
