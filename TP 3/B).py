import numpy as np
import igraph
import networkx as nx
from Func import clusterize
import matplotlib.pylab as plt

G = nx.read_gml("dolphins.gml")

metodos= ['infomap', 'fastgreedy', 'louvain', 'edge_betweenness']
##Diccionarios de distintas comunidades
GI = clusterize(G, method=metodos[0])
GFG = clusterize(G,method=metodos[1])
GL = clusterize(G,method=metodos[2])
GE = clusterize(G,method=metodos[3])


### Armo el grafo en igraph para usarlo como argumento de la función de modularidad
G_aux = igraph.Graph()
G_aux.add_vertices(list(G.nodes))
G_aux.add_edges(list(G.edges))


comunidades  = [list(GI.values()), list(GFG.values()), list(GL.values()), list(GE.values())]

Q_infomap = igraph.Graph.modularity(G_aux,comunidades[0])
Q_fastgreedy = igraph.Graph.modularity(G_aux,comunidades[1])
Q_louvain = igraph.Graph.modularity(G_aux,comunidades[2])
Q_edge_betweenness = igraph.Graph.modularity(G_aux,comunidades[3])

Q_todas=[Q_infomap, Q_fastgreedy, Q_louvain, Q_edge_betweenness]


print("La modularidad dado el método Infomap es:", Q_todas[0])
print("La modularidad dado el método Fast-Greedy es:", Q_todas[1])
print("La modularidad dado el método Louvain es:", Q_todas[2])
print("La modularidad dado el método Edge Betweenness es:", Q_todas[3])

Qes=[]
M=10000
nro_enlaces=len(G.edges())
for i in range(M):
    G_sw=nx.swap.double_edge_swap(G, nswap=nro_enlaces, max_tries=1000)
    nodos_cluster = clusterize(G_sw, metodos[3])## j=0:infomap; j=1:fastgreedy; j=2:louvain; j=3:edge_betweenness
    comunidades=list(nodos_cluster.values())
    G_sw_aux = igraph.Graph()
    G_sw_aux.add_vertices(list(G_sw.nodes))
    G_sw_aux.add_edges(list(G_sw.edges))
    try: ##esto porque en edge_betweenness da error si la comunidad no tiene la longitud deseada
        Q = igraph.Graph.modularity(G_sw_aux,comunidades)
        Qes.append(Q)
    except:
        print("oh no")
   


   

	


bins = np.arange(min(Qes)-0.05 , max(Qes)+0.05, 0.001)



Num,Cen=np.histogram(Qes,bins=bins)
plt.title("Modularidad método Edge-Betweenness")
plt.axvline(Q_todas[3], c="red")## j=0:infomap; j=1:fastgreedy; j=2:louvain; j=3:edge_betweenness
plt.hist(Qes,bins=bins)
plt.legend(['Modularidad red real'])
plt.xlabel('Modularidad')
plt.ylabel('Repeticiones')
plt.show()