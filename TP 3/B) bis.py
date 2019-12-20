import numpy as np
import igraph
import networkx as nx
from func import mem
from func import sil
from func import clusterize
import matplotlib.pylab as plt

G = nx.read_gml("dolphins.gml")


metodos= ['infomap', 'fastgreedy', 'louvain', 'edge_betweenness']
##Diccionarios de distintas comunidades
GI = clusterize(G, method=metodos[0])
GFG = clusterize(G,method=metodos[1])
GL = clusterize(G,method=metodos[2])
GE = clusterize(G,method=metodos[3])

cluster_nodos=dict()
for k in range(max(list(GI.values()))+1):
    delf=[]
    for x in GI.items():
        if x[1]==k:
            delf.append(x[0])
    cluster_nodos[k]=delf

print(cluster_nodos)


D = {}
for k in cluster_nodos.keys():
    D[k]=[]

for nodo in G.nodes():
    C = mem(nodo, cluster_nodos)
    D[C].append([nodo,sil(nodo,G,cluster_nodos)])
#    print(sil(nodo, G, cluster_nodos))

L = {}
for k in D.keys():
    l = D[k]
    l.sort(key=lambda x:x[1])
    L[k] = l


#Lista de nombres de los nodos para usar en el gráfico
x=[x[0] for x in L[1]]
x_nodos=[i for i in range(len(x))]

y=[y[1] for y in L[1]]


fig, ax = plt.subplots()
plt.ylabel("Silhouette")
plt.axhline(y=np.mean(y), color='r', linestyle='-')
plt.legend("Silhouette media red real", loc='upper left')

plt.xticks(x_nodos, x, rotation='vertical')

ax.fill_between(x_nodos, y)


plt.show()







