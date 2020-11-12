from state import State


class Agent:
    # When an agent move from vertex v1 to v2 thorough an edge with weight w we immediately move it's location to v2
    # and freeze him there for w-1 time units.

    def __init__(self, aid):
        self.aid = aid
        self.terminated = False
        self.saver = True  # Does the agent save people

    def act(self, observation):
        return None

    def observe(self, state):
        return state

    def terminate(self):
        self.terminated = True

    def is_terminated(self):
        return self.terminated

    def is_moving(self, obseravtion: State):
        location = obseravtion.locations[self.aid]
        # If the agent has more than 0 steps, that means he is now moving on an edge
        return location[2] > 0
