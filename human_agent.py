from agent import Agent


class HumanAgent(Agent):

    def act(self, observation):
        if self.frozen_time_remaining > 0:
            self.frozen_time_remaining -= 1
            return None
        self.print_observation(observation)
        self.print_neighbors(observation)
        chosen_vertex = int(input("Please select a vertex to move to"))
        current_vertex = observation.locations[self.id]
        # TODO get actual weight of edge
        weight = 1
        return [current_vertex, chosen_vertex, weight]

    def print_observation(self, observation):
        my_location = observation.locations[self.id]


