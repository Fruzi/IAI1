class Graph:
    def __init__(self, numofvertices, bidirected=False):
        self.edges = []  # A list of dictionaries where the key is a neighbour vertex id and the value is edge weight
        self.vertices_values = []  # The key is vertex id and the value vertex value
        self.bidrected = bidirected
        for i in range(numofvertices):
            self.edges.append({})

    def add_vertex(self, vertexid, value=0):
        # We keep vetexid parameter for debugging purposes, although we add vertices by their order: 0,1,2,...
        self.vertices_values.append(value)

    def add_edge(self, v1, v2, weight):
        self.edges[v1][v2] = weight
        if self.bidrected:
            self.edges[v2][v1] = weight

    def get_neighbours(self, vertexid):
        return self.edges[vertexid]

    def get_vertex_value(self, vertexid):
        return self.vertices_values[vertexid]
