import matplotlib.pyplot as plt
import networkx as nx


class State:
    def __init__(self, graph, locations, deadline=-1, time=0):
        self.time = time
        self.graph = graph
        # Location is a tuple (origin node, destination node, steps left to reach dest), when we have 0 steps left, that
        # means we reached the dest and now in it
        # Example of agent in node: [2,3,0] - agent came from v2, now in v3
        # Example of agent in edge: [2,3,5] - agent arriving to v3 from v2 in 5 steps (time-units)
        self.locations = locations
        self.deadline = deadline
        self.people_remaining = sum(node[1]['value'] for node in graph.nodes.data())

    def advance_time(self, time_units=1):
        self.time += time_units

    def is_deadline_reached(self):
        return self.deadline != -1 and self.time >= self.deadline

    def block_road(self, vertex1id, vertex2id):
        self.graph.remove_edge(vertex1id, vertex2id)

    def print(self):
        print('-' * 20)
        print(f"Current Time: {self.time}")
        print(f'{self.people_remaining} people need saving')
        # Print location of every agent
        for i in range(len(self.locations)):
            if self.locations[i][2] == 0:
                print(f"Agent {i} is at node {self.locations[i][1]}")
            else:
                print(
                    f"Agent {i} is at edge {self.locations[i][0]}-{self.locations[i][1]} with {self.locations[i][2]} steps left")
        self.draw_graph()

    def draw_graph(self):
        """
        Draws the graph on the screen
        """
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos, node_size=700)
        nx.draw_networkx_edges(self.graph, pos, edgelist=self.graph.edges(data=True), width=4)
        edgelist = {edge: f"w{self.graph[edge[0]][edge[1]]['weight']}e{self.graph[edge[0]][edge[1]]['eid']}" for edge in
                    self.graph.edges}
        nx.draw_networkx_edge_labels(self.graph, pos, edgelist)
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_family="sans-serif")
        plt.show()
