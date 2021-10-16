from collections import defaultdict


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)
        # self.graph[v].append(u)

        return self.graph

    def BFS(self, g):
        # queue for dfs not visited nodes
        queue = []
        visited = set()

        # connected component
        for val in range(len(g)):
            if val not in visited:
                visited.add(val)
                
                # mark the val to visited
                queue.append(val)

                # For every node in queue visit nodes adjacent list add in q if not visited, n mark visited
                while queue:
                    val = queue.pop(0)
                    print(val, end=" ")

                    for i in self.graph[val]:
                        # if adjacent nodes not visited
                        if i not in visited:
                            queue.append(i)
                            visited.add(i)
            print()


g = Graph()
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 2)
g.addEdge(2, 0)
g.addEdge(2, 3)
g.addEdge(4, 5)
graph = g.addEdge(3, 3)


g.BFS(graph)
