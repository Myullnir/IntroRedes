import igraph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from func import clusterize

G = nx.read_gml("dolphins.gml")

# INFOMAP-----------------------------------------------------

# Ojo! los clusters pueden cambiar cada vez que se
# corra la siguiente linea:
G_cd = clusterize(G)

nx.draw_networkx(G,node_color = list(G_cd.values()),labels = G_cd)

# Modularidad--------------------------------------------
membership = list(G_cd.values())
g = igraph.Graph()
g.add_vertices(list(G.nodes))
g.add_edges(list(G.edges))
Q = igraph.Graph.modularity(g,membership)

# Silhouette---------------------------------------------

#cluster_nodos = {comunidad: [lista de sus nodos]}
cluster_nodos = {}
for c,x in zip(membership,G.nodes()):
    try: 
        cluster_nodos[c].append(x)
    except:
        cluster_nodos[c] = [x]

#me fije en la pag:
#https://stackoverflow.com/questions/11597785/setting-spacing-between-grouped-bar-plots-in-matplotlib
groups = [[sil(x) for x in cluster_nodos[c]] for c in cluster_nodos.keys()]
group_labels = [str(c) for c in cluster_nodos.keys()]












## Fast Greedy
#G_cd = clusterize(G,method="fastgreedy")
#nx.draw_networkx(G,node_color = list(G_cd.values()),labels = G_cd)
#
## Louvain
#G_cd = clusterize(G,method="louvain")
#nx.draw_networkx(G,node_color = list(G_cd.values()),labels = G_cd)
#
## Edge Betweenness
#G_cd = clusterize(G,method="edge_betweenness")
#nx.draw_networkx(G,node_color = list(G_cd.values()),labels = G_cd)
#
## Plot:
##plt.show()

