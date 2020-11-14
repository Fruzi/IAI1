from graphreader import GraphReader
from human_agent import HumanAgent
from simulator import Simulator
from astar_agent import AStarAgent
from greedy_heuristic_agent import GreedyHeuristicAgent
from state import State


def update(actions, agents, state):
    if state.time == 0:  # People at starting positions of saving agents are automatically saved
        for i in range(len(agents)):
            if agents[i].saver and state.graph.nodes[state.locations[i][1]]['value']:
                savedpeople = state.graph.nodes[state.locations[i][1]]['value']
                state.graph.nodes[state.locations[i][1]]['value'] = 0
                state.people_remaining -= savedpeople
                agents[i].add_people(savedpeople)

    # update all moving agents
    for i in range(len(state.locations)):
        if state.locations[i][2] > 0:
            state.locations[i][2] -= 1

    for i in range(len(actions)):
        action = actions[i]
        # No-op happens when an agent is terminated, frozen (saboteur at the start), or moving on an edge
        if action[0] != "noop":
            if action[0] == "move":
                # -1 because the when we decide to traverse an edge we already make the first step on it.
                # This also makes it so edges with weight=1 would take 1 turn, which means that the next action would
                # also be meaningful and not traversing no-op
                state.locations[i] = [action[1], action[2], action[3] - 1]
            elif action[0] == "block":
                # Block action of saboteur which removes an edge from the graph, if another agent is on it, it will
                # continue, but no one would be able to choose the edge once it's destroyed
                state.graph.remove_edge(action[1], action[2])
            elif action[0] == "terminate":
                # Location -1 represents a terminated agent alongside the terminated data member
                state.locations[i] = [-1, -1, 0]

        # If a saving agent is at (or just arrived to) a location that has people to save
        if agents[i].saver and state.locations[i][2] == 0 and state.graph.nodes[state.locations[i][1]]['value']:
            savedpeople = state.graph.nodes[state.locations[i][1]]['value']
            state.graph.nodes[state.locations[i][1]]['value'] = 0
            state.people_remaining -= savedpeople
            agents[i].add_people(savedpeople)
    state.advance_time()
    return state


def terminate(state):
    # If the deadline is reached
    return state.is_deadline_reached() or state.people_remaining <= 0 or all(loc[0] == -1 for loc in state.locations)


def stupid(a, b):
    return 0


if __name__ == '__main__':
    graph, deadline = GraphReader().read(r"C:\Users\Uzi\Desktop\exampleg.txt")
    agents_locations = [(0, 0, 0), (2, 2, 0)]
    state = State(graph, agents_locations)
    agents = [HumanAgent(0), GreedyHeuristicAgent(1)]
    Simulator().run_environment(state, update, agents, terminate)
