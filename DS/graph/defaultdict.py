# from collections import defaultdict



# def Graph(u,v,g):
#     graph = g

#     graph[u].append(v)
#     graph[v].append(u)
#     return graph

# def traverse(graph):
#     for key,value in graph.items():
#         print(key,value)
#     # print(graph)
        


# graph = defaultdict(list)
# graph = Graph(0,1,graph)
# graph = Graph(0,2,graph)
# graph = Graph(1,2,graph)
# graph = Graph(1,3,graph)
# graph = Graph(2,4,graph)
# graph = Graph(1,4,graph)
# graph = Graph(3,4,graph)

# traverse(graph)

class Graph:

    def __init__(self):
        self.name = None

    def setName(self):
        self.name = "vikram"
    
    def returnname(self):
        return self.name
k  = Graph()

k.setName()
p = k.returnname()

print(p)