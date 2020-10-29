from math import inf

import networkx as nx

from graphreader import GraphReader


def dijkstra(g, start):
    def backtrace(prev1, start1, end):
        node = end
        path1 = []
        while node != start1:
            path1.append(node)
            node = prev1[node]
        path1.append(node)
        path1.reverse()
        return path1

    def cost(u, v):
        return g.get_edge_data(u, v).get('weight')

    prev = {}
    dist = {v: inf for v in list(nx.nodes(g))}
    visited = set()
    dist[start] = 0
    pd = {start: dist[start]}
    curr = None
    while pd:
        curr = min(pd, key=pd.get)
        pd.pop(curr)
        if g.nodes[curr]["value"] != 0 and curr != start:
            break
        visited.add(curr)
        for neighbor in dict(g.adjacency()).get(curr):
            path = dist[curr] + cost(curr, neighbor)
            if path < dist[neighbor]:
                dist[neighbor] = path
                prev[neighbor] = curr
                if neighbor not in visited:
                    visited.add(neighbor)
                pd[neighbor] = dist[neighbor]
    npath = backtrace(prev, start, curr)
    sequence = []
    for i in range(len(npath) - 1):
        sequence.append((npath[i], npath[i + 1], g.edges[npath[i], npath[i + 1]]['weight']))
    print(sequence)


if __name__ == '__main__':
    graph, deadline = GraphReader().read(r"C:\Users\Lior\Desktop\v2.txt")
    dijkstra(graph, 0)
