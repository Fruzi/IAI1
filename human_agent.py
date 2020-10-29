from agent import Agent


class HumanAgent(Agent):

    def act(self, observation):
        if self.frozen_time_remaining > 0:
            self.frozen_time_remaining -= 1
            return None
        print("The entire graph is:\n")
        self.print_observation(observation)
        print("My current neighbors are:\n")
        self.print_neighbors(observation)
        current_vertex = observation.locations[self.id]
        legal = False
        while not legal:
            chosen_vertex = int(input("Please select a vertex to move to or type \'terminate\'"))
            if chosen_vertex == 'terminate':
                self.terminate()
                return chosen_vertex
            if chosen_vertex not in observation.graph.get_neighbours(current_vertex):
                print("Please choose a legal vertex to move to")
            else:
                legal = True
        # TODO get actual weight of edge
        weight = 1
        return [current_vertex, chosen_vertex, weight]

    def print_neighbors(self, observation):
        # TODO make work
        my_location = observation.locations[self.id]
        neighbors = observation.graph.adjacency().get(my_location)
        print(neighbors)


