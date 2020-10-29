from graph import Graph


class GraphReader:
    def read(self, path):
        with open(path, 'r') as f:
            templine = self.formatline(f.readline())
            numofvertices = int(templine[1])
            templine = self.formatline(f.readline())
            deadline = float(templine[1])

            graph = Graph(numofvertices, bidirected=True)
            reading_vertices = True  # Do we read vertices or edges
            for line in f:
                line = self.formatline(line)
                if line:  # The line that marks the switch is a blank line
                    if reading_vertices:  # Currently reading the vertices
                        vertexid = int(line[0][1:])
                        if len(line) == 1:  # A vertex without people
                            graph.add_vertex(vertexid)
                        else:
                            graph.add_vertex(vertexid, int(line[1][1:]))
                    else:  # Currently reading the edges
                        vertex1id = int(line[1])  # First vertex id
                        vertex2id = int(line[2])  # Second vertex id
                        weight = int(line[3][1:])  # Edge cost
                        graph.add_edge(vertex1id, vertex2id, weight)
                else:
                    reading_vertices = False
            return graph, deadline

    def formatline(self, line: str):
        if line.startswith('#'):
            return line[1:].split(';')[0].strip().split()  # Remove the comment if there is one and split into the parts
        else:  # The empty line that marks the switch from vertices to edges
            return ''

