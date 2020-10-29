from agent import Agent


class HumanAgent(Agent):

    def act(self, observation):
        self.print_observation(observation)

