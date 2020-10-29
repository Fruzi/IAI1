from human_agent import HumanAgent
from greedy_agent import GreedyAgent
from saboteur_agent import SaboteurAgent
from state import State


class Simulator:
    AGENTS = {'human': HumanAgent, 'greedy': GreedyAgent, 'saboteur': SaboteurAgent}

    def __init__(self, graph, time_limit):
        self.time_limit = time_limit
        self.agents = []
        self.state = None
        num_agents = input("Enter number of agents")
        locations = []
        for i in range(0, int(num_agents)):
            agent_name = input("enter name of agent number {}".format(i))
            if agent_name in self.AGENTS:
                self.agents.append(self.AGENTS[agent_name](i))
                initial_location = input("enter vertex id for initial agent location")
                locations.append(int(initial_location))
        self.generate_initial_state(graph, locations)
        self.rewards = [0] * num_agents

    def generate_initial_state(self, graph, locations):
        self.state = State(graph, locations)

    def run_sequential_environment(self):
        while not self.terminated():
            for agent in self.agents:
                observation = agent.observe(self.state)
                action = agent.act(observation)
                self.update_state(agent, action)

    def run_simultaneously_environment(self):
        while not self.terminated():
            actions = []
            for agent in self.agents:
                observation = agent.observe(self.state)
                actions.append([agent, agent.act(observation)])
            for agent, action in actions:
                self.update_state(agent, action)

    def update_state(self, agent, action):
        self.state.advance_time()
        if action is None:
            return None
        if action is "terminated":
            # Calculate if your final move rescued any people. Handles the edge case where you
            # are unfrozen and the game ends
            final_reward = self.state.locations[agent.id].value
            self.rewards[agent.id] += final_reward
            self.state.people_remaining -= final_reward
        # I'm assuming that move actions are represented as a tuple of vertices and weight [origin, destination, weight]
        # TODO make sure this complies with the representation of graphix
        self.state.locations[agent.id] = action[1]
        # Update the agent's reward
        self.rewards[agent.id] += action[0].value
        # Update the number of people remaining in the graph
        self.state.people_remaining -= action[0].value

    def terminated(self):
        # Check if time limit has passed
        if self.state.time > self.time_limit:
            return True
        # Check if there are no more people to rescue
        if self.state.people_remaining == 0:
            return True
        # Check if all agents terminated
        all_done = True
        for agent in self.agents:
            if not agent.terminated():
                all_done = False
                break
        if all_done:
            return True
        # No termination condition was found
        return False

    def print_state(self):
        return None
