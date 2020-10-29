class Agent:
    # When an agent move from vertex v1 to v2 thorough an edge with weight w we imidiatly move it's location to v2
    # and freeze him there for w-1 time units.

    def __init__(self, id):
        self.terminated = False
        self.frozen_time_remaining = 0
        self.id = id

    def act(self, observation):
        return None

    def observe(self, state):
        return state

    def terminate(self):
        self.terminated = True

    def is_terminated(self):
        return self.terminated

    def print_observation(self, observation):
        print(observation)
