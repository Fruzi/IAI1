import math

from agent import Agent
from state import State


class SaboteurAgent(Agent):
    def __init__(self, aid, no_ops=0):
        super().__init__(aid)
        self.no_ops = no_ops
        self.blocked_last_action = False
        self.saver = False

    def act(self, observation: State):
        if self.terminated:  # If terminated, return no-op
            return ("noop",)
        if observation.time < self.no_ops:  # If frozen in the start, return no-op
            return ("noop",)
        if self.is_moving(observation):  # if traversing on edge, return no-op
            return ("noop",)
        if self.blocked_last_action:  # If he blocked last action, it needs to move
            self.blocked_last_action = False
            # If the agent is not traversing, it reached its dest and the dest is its current location
            currloc = observation.locations[self.aid][1]
            neighbour_edges = observation.graph[currloc]
            # If there are no neighbours to the current node, meaning no edges from it, terminate the agent
            if len(neighbour_edges) == 0:
                self.terminated = True
                return ("terminate",)
            # Find the lowest cost neighbour and return it and its edge weight
            dest, weight = self.find_min_edge(neighbour_edges)
            return ("move", currloc, dest, weight)
        else:  # If not blocked last action, it needs to block
            self.blocked_last_action = True
            currloc = observation.locations[self.aid][1]
            neighbour_edges = observation.graph[currloc]
            # Find the lowest cost neighbour and return it and its edge weight, but just keep the neighbour because we
            # are destroying the edge
            dest, _ = self.find_min_edge(neighbour_edges)
            return ("block", currloc, dest)

    def find_min_edge(self, neighbour_edges):
        """
        :param neighbour_edges: Dict of neighbour and edge data, for example for neighbour_edges:
        {2: {'eid': 2, 'weight': 1}, 1: {'eid': 5, 'weight': 5}}
        :return: The neighbour with the lowest cost edge and the edge's weight
        """
        mindest = None
        minweight = math.inf
        for dest in neighbour_edges:
            weight = neighbour_edges[dest]["weight"]
            if weight < minweight:
                mindest = dest
                minweight = weight
            # If two edges have the same weight, we prefer the one with lower id (which cannot be identical)
            elif weight == minweight:
                if neighbour_edges[dest]["eid"] < neighbour_edges[mindest]["eid"]:
                    mindest = dest
                    minweight = weight
        return mindest, minweight
