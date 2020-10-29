from agent import Agent
from dijkstra import dijkstra

class GreedyAgent(Agent):

    def __init__(self):
        super().__init__()
        self.greedy_path = []

    def act(self, state):
        if self.frozen_time_remaining > 0:
            self.frozen_time_remaining -= 1
            return None
        if self.greedy_path is []:
            graph = state.graph
            location = state.locations[self.id]
            self.greedy_path = dijkstra(graph, location)
        action = self.greedy_path[0]
        # TODO adapt this to match the representation of path via graphix
        self.greedy_path = self.greedy_path[1:]
        self.frozen_time_remaining = action[2] - 1
        return action


