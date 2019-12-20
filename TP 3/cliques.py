import networkx as nx
import copy
import random

G = nx.read_gml("dolphins.gml")


# Al principio, cada nodo es su propio cluster
# rg = [0,1,2,...,Nnodos-1]
rg = range(len(G.nodes()))
clusters = [k:[x] for k,x in zip(rg,G.nodes())]
## Como lo unico que nos importa es maximizar Q,
## podemos empezar de un Q cualquiera
#Q = 0

from func_cliques import dq

for x in G.nodes():
    kx = 0
    for k in clusters.keys():
        if x in clusters[k]:
            kx = k
    # kx = nro del cluster que tiene a x
    K = []
    k = 0
    m = 0
    for k in clusters.keys():
        C = clusters[k]
        if dq(x,G,C) == m:
            K.append(k)
        elif dq(x,G,C) > m:
            K = [k]
            m = dq(x,G,C)
    km = random.choice(K)
    clusters[kx].remove(x)
    clusters[km].append(x)
    for k in clusters.keys():
        if clusters[k] == []:
            del clusters[k]

