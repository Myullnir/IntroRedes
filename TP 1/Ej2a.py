import numpy as np
import networkx as nx
import matplotlib.pylab as plt
import random

def ldata(archive):
        f=open(archive)
        data=[]
        for line in f:
            line=line.strip()
            col=line.split()
            data.append(col)	
        return data
    
delf=ldata("dolphinsGender.txt")
G = nx.read_gml('dolphins.gml')
delf.sort()

for delfin in G.nodes():
    for genero in delf:
        if genero[0]==delfin:
            G.nodes[delfin]["genero"]=genero[1]



nx.draw(G, 
        width=1, 
        node_color=["blue" if g=="m" else "red" if g=="f" else "yellow" for g in nx.get_node_attributes(G, "genero").values()], 
        node_size=150,
        with_labels=False)
plt.title("Grafo simple")
plt.show()


nx.draw_circular(G, 
        width=1, 
        node_color=["blue" if g=="m" else "red" if g=="f" else "yellow" for g in nx.get_node_attributes(G, "genero").values()], 
        node_size=150,
        with_labels=False)
plt.title("Grafo layout circular")
plt.show()

#Todos los nodos a distancias similares y la menor cantidad de enlaces cruzados posibles
nx.draw_spring(G, 
        width=1, 
        node_color=["blue" if g=="m" else "red" if g=="f" else "yellow" for g in nx.get_node_attributes(G, "genero").values()], 
        node_size=150,
        with_labels=False)
plt.title("Grafo layout spring")
plt.show()

#Todos los nodos se van agrupando segùn similitud
nx.draw_spectral(G, 
        width=1, 
        node_color=["blue" if g=="m" else "red" if g=="f" else "yellow" for g in nx.get_node_attributes(G, "genero").values()],
        node_size=150,
        with_labels=False)
plt.title("Grafo layout spectral")
plt.show()

nx.draw_random(G, 
        width=1, 
        node_color=["blue" if g=="m" else "red" if g=="f" else "yellow" for g in nx.get_node_attributes(G, "genero").values()],
        node_size=150,
        with_labels=False)
plt.title("Grafo random")
plt.show()

