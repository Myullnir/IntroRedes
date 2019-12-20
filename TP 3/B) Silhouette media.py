import numpy as np
import networkx as nx
from func import mem
from func import sil
from func import clusterize


G = nx.read_gml("dolphins.gml")


metodos= ['infomap', 'fastgreedy', 'louvain', 'edge_betweenness']
##Diccionarios de distintas comunidades
GI = clusterize(G, method=metodos[0])
GFG = clusterize(G,method=metodos[1])
GL = clusterize(G,method=metodos[2])
GEB = clusterize(G,method=metodos[3])

cluster_nodos=dict()
for k in range(max(list(GEB.values()))+1):###Acá hay que cambiar GI, GFG, GL, GEB
    delf=[]
    for x in GI.items():
        if x[1]==k:
            delf.append(x[0])
    cluster_nodos[k]=delf
    
    
S=[]
print(cluster_nodos)
for nodo in G.nodes():
    try:
        S.append(sil(nodo, G, cluster_nodos))
    except:
        None
    
print(S)
media=np.mean(S)
print("Silhouette media total Edge-Betweenness:", media)