from human_agent import HumanAgent
from greedy_agent import GreedyAgent
from saboteur_agent import SaboteurAgent
from state import State


class Simulator:
    AGENTS = {'human': HumanAgent, 'greedy': GreedyAgent, 'saboteur': SaboteurAgent}

    def __init__(self, graph, time_limit):
        self.time_limit = time_limit
        self.agents = []
        num_agents = input("Enter number of agents")
        locations = []
        for i in range(0, int(num_agents)):
            agent_name = input("enter name of agent number {}".format(i))
            if agent_name in self.AGENTS:
                self.agents.append(self.AGENTS[agent_name]())
                initial_location = input("enter vertex id for initial agent location")
                locations.append(int(initial_location))
        self.generate_initial_state(graph, locations)

    def generate_initial_state(self, graph, locations):
        return State(graph, locations)

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
        

    def terminated(self):
        if self.state.time > self.time_limit:
            return True
        #     if no more people to rescue:
        #       return True
        return False

    def print_state(self):
        return None
