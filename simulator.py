class Simulator:
    def __init__(self):
        pass

    def run_environment(self, state, updatefn, agents, terminationfn):
        for agent in agents:
            print(state.locations[agent.aid][1])
            if state.graph.nodes(data=True)[state.locations[agent.aid][1]]['value'] > 0:
                people_saved = state.graph.nodes(data=True)[state.locations[agent.aid][1]]['value']
                agent.add_people(people_saved)
                state.graph.nodes(data=True)[state.locations[agent.aid][1]]['value'] = 0
                state.people_remaining -= people_saved
        while True:
            state.print()
            for agent in agents:
                agent.print()
            # Generate observations for all agents
            observations = [agent.observe(state) for agent in agents]
            # Generate actions for all agents given their respective observations
            actions = []
            for i in range(len(agents)):
                actions.append(agents[i].act(observations[i]))
            # Update the state
            state = updatefn(actions, agents, state)
            if terminationfn(state):  # Terminate if needed
                state.print()
                for agent in agents:
                    agent.print()
                print("END OF RUN")
                break
