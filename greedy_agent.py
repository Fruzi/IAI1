from agent import Agent


class GreedyAgent(Agent):


    def act(self, state):
        if self.frozen_time_remaining > 0:
            self.frozen_time_remaining -= 1
        else:
