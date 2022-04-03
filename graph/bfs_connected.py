from collections import defaultdict


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)
        # self.graph[v].append(u)

        return self.graph

    def BFS(self):
        # queue for dfs visited nodes
        queue = []
        visited = set()

        # connected component, running loop for every not seeen nodes in graph
        # suppose one connected component is fully traversed,
        # so two print other component we need to run loop for every node if it's not visited
        for val,_ in list(self.graph.items()):
            if val not in visited:
                # mark the val to visited
                visited.add(val)
                
                queue.append(val)

                # For every node in queue visit nodes adjacent list add in q if not visited, n mark visited
                while queue:
                    val = queue.pop(0)
                    print(val, end=" ")

                    # every adjacent node list
                    for i in self.graph[val]:
                        # if adjacent nodes not visited
                        if i not in visited:
                            queue.append(i)
                            visited.add(i)
            print()


g = Graph()
g.addEdge(1, 2)
g.addEdge(2, 3)
g.addEdge(3, 5)
g.addEdge(5, 7)
g.addEdge(4, 6)
g.addEdge(6, 8)

# graph = g.addEdge(3, 4)


g.BFS()
