class Simulator:
    def __init__(self):
        pass

    def run_environment(self, state, updatefn, agents, terminationfn):
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
