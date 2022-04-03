from  collections import defaultdict
class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)
        # self.graph[v].append(u)

        return self.graph

def dfsutil(graph,v,visited):

    print(v,end=" ")

    for neighbor in graph[v]:
        if neighbor not in visited:
            visited.add(neighbor)
            dfsutil(graph,neighbor,visited)

def dfs(graph):
    visited = set()

    for i in range(1,len(graph)+1):
        if i not in visited:
            visited.add(i)
            dfsutil(graph,i,visited)

g = Graph()
g.addEdge(1, 2)
g.addEdge(2, 4)
g.addEdge(2, 7)
g.addEdge(4, 6)
g.addEdge(6, 7)
graph = g.addEdge(3, 5)
dfs(graph)