from agent import Agent


class HumanAgent(Agent):
    def act(self, observation):
        location = observation.locations[self.aid]
        if location[2] != 0:
            return ("noop",)
        neighbors = observation.graph[location[1]]
        neighbor_nodes = [str(n) for n in neighbors]
        print(f"Human agent {self.aid}, your neighbouring nodes are: {','.join(neighbor_nodes)}")
        while True:
            dest = input(f"Where do you want to go: ")
            if dest not in neighbor_nodes:
                print("Please enter a valid node id")
            else:
                break
        dest = int(dest)
        return ("move", location[1], dest, neighbors[dest]['weight'])
