"""
Pros: Saves space O(|V|+|E|) . 
In the worst case, there can be C(V, 2) number of edges in a graph 
thus consuming O(V^2) space. Adding a vertex is easier.
Cons: Queries like whether there is an edge from vertex u 
to vertex v are not efficient and can be done O(V).
"""
# AdjacencyList for graph

class VertexNode:
    def __init__(self,vertex):
        self.vertex = vertex
        self.next = None

class Graph:
    def __init__(self,vertex):
        self.vertex = vertex
        self.graph = [None]*self.vertex

    # adding edge from src to destination
    def addEdge(self,src,dest):
        # create a node
        node = VertexNode(dest)
        # add previous list reference to new vertex next (which is stored in graph[src] 0 [dc12] --> [0|NULL] address dc12)
        # 0 --> 1 adding the addres of 1 in the next of 2.
        # 0 --> 2 1 after adding link (0,2)
        node.next = self.graph[src]
        # add the address of 2 or updated list ie 2 1 to graph[src] = 0
        self.graph[src] = node

    # similary add edge det to src
        node = VertexNode(src)
        node.next = self.graph[dest]
        self.graph[dest] = node

    def output(self):
        for i in range(self.vertex):
            temp = self.graph[i]
            print(str(i)+" --> ",end="")
            while temp:
                print(temp.vertex,end=" ")
                temp = temp.next
            print(end="\n")



# method2
from collections import defaultdict
# This class represents a directed graph
# using adjacency list representation
class Graph1:
 
    # Constructor
    def __init__(self):
 
        # default dictionary to store graph
        self.graph = defaultdict(list)
 
    # function to add an edge to graph
    def addEdge(self,u,v):
        self.graph[u].append(v)

if __name__ == '__main__':
    graph = Graph(5)
    graph.addEdge(0, 4)
    graph.addEdge(0, 1)
    graph.addEdge(1, 2)
    graph.addEdge(1, 3)
    graph.addEdge(1, 4)
    graph.addEdge(2, 3)
    graph.addEdge(3, 4)

    graph.output()