import networkx as nx
import matplotlib as plt

G = nx.Graph()
G.add_nodes_from([1,2,3,4])
G.add_edges_from([(1,2), (2,3), (3,1), (4,1)])
#G.add_edges_from([(1, 2), (2, 3), (3, 1)])
nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()

C0=nx.clustering(G,3)
print(C0)
#C=nx.average_clustering(G)
#print(C)
