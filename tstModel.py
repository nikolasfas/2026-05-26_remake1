from model.model import Model

myModel = Model()
myModel.buildGraph(1.2 , 2.7)
nodes, edges = myModel.getGraphDetails()

print(f"Number of nodes: {len(nodes)}")
print(f"Number of edges: {len(edges)}")