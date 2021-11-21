from collections import defaultdict,deque


class Node:
    def __init__(self):
        self.graph = defaultdict(list)

    def addedge(self,u,v):
        self.graph[u].append(v)

def detectcycledfs(graph,v,visited):
    parent = [-1]*len(graph)

    q = deque()
    q.append(v)

    while q:
        u = q.popleft()

        for neighbor in graph[v]:
            if neighbor not  in visited:
                # add adjacent node to visited
                visited.add(neighbor)
                # add adjacent node to q
                q.append(neighbor)
                parent[neighbor] = u

            # since adjacent node is visited already check if adjacent node
            # parent is previous node, if not then there is cycle 
         
            elif parent[neighbor] == u:
                return True
    return False


def dfsutility(graph,v):
    visited = set()
    for node in graph:
        if node not in visited:
            visited.add(node)
            detectcycledfs(graph,node,visited)




