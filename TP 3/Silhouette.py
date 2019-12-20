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



#Suponiendo que tengo cluster_nodos, calculo silouette para cada metodo
import csv
D = {}
for k in cluster_nodos.keys():
    D[k]=[]

for nodo in G.nodes():
    C = mem(nodo, cluster_nodos)
    D[C].append([nodo,sil(nodo,G,cluster_nodos)])

L = {}
for k in D.keys():
    l = D[k]
    l.sort(key=lambda x:x[1])
    L[k] = l



#bins = np.arange(min(L[0])-0.05 , max(L[0])+0.05, 1)



#Num,Cen=np.histogram(L[0])#,bins=bins)
#plt.title("Modularidad método Edge-Betweenness")
#plt.axvline(Q_todas[3], c="red")## j=0:infomap; j=1:fastgreedy; j=2:louvain; j=3:edge_betweenness
plt.plot([x[1] for x in L[1]])#,bins=bins)
#plt.legend(['Modularidad red real'])
#plt.xlabel('Modularidad')
#plt.ylabel('Repeticiones')
plt.show()
