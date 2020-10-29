class Agent:

    def __init__(self):
        self.terminated = False
        self.frozen_time_remaining = 0

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
