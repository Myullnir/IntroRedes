import igraph
import networkx as nx
import matplotlib.pyplot as plt
from func import clusterize

G = nx.read_gml("dolphins.gml")

# Infomap
G_cd = clusterize(G)
nx.draw_networkx(G,node_color = list(G_cd.values()),
	               with_labels = False)
# Fast Greedy
G_cd = clusterize(G,method="fastgreedy")
nx.draw_networkx(G,node_color = list(G_cd.values()),
	               with_labels = False)

# Louvain
G_cd = clusterize(G,method="louvain")
nx.draw_networkx(G,node_color = list(G_cd.values()),
	               with_labels = False)

# Edge Betweenness
G_cd = clusterize(G,method="edge_betweenness")
nx.draw_networkx(G,node_color = list(G_cd.values()),
	               with_labels = False)

# Plot:
#plt.show()