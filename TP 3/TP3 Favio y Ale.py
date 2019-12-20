# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 10:29:59 2018

@author: Fabio
"""

import networkx as nx
import math
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import community



  
def ldata(archive):
        f = open(archive)
        data = []
        for line in f:
            col = line.split("\t")
            col = [x.strip() for x in col]
            data.append(col)
        return data 


G=nx.read_gml("dolphins.gml")
Gen=ldata("dolphinsGender.txt")

## Partición en clusters
## Algoritmo de Louvain


part = community.best_partition(G)

# Lista de delfines con grupo

partl=[[x[0],x[1]] for x in part.items()]

# Ordenamos la lista

partl.sort(key=lambda x:x[1])

# Separemos la lista en colores segùn clusters

Col=["r","p","g","o","y","m"]

# Col es la lista de los nombres de los colores
# LCol es la lista con las listas de delfines asociados a cada color
# Segun la comunidad a la que pertenecen
r=[]
p=[]
g=[]
o=[]
y=[]
m=[]


LCol=[r,p,g,o,y,m]

# Com es la lista de las comunidades 
#que estaban asiganadas a los delfines y ordenadas

Com=[x[1] for x in partl]

m=0

# Con este comando voy asignando delfines a cada una de las listas
# de colores según su comunidad, usando el hecho de 
# que sé que mi lista partl y Com están ordenadas

for j in range(partl[len(partl)-1][1]+1):
    N=Com.count(j)
    for l in range(m,N+m):
        LCol[j].append(partl[l][0])
    m=N+m


# Con esto asigno géneros a los delfines

for delf in Gen:
    for x in G.nodes.data():
        if x[0]==delf[0]:
            G.nodes[x[0]]["genero"] = delf[1]
            

# Armo un diccionario de delfines con labels

Gend=dict()

for delf in G.nodes.data("genero"):
    Gend[delf[0]]=delf[1]


# Acá simplemente armo el gráfico y ploteo

nx.draw(G, 
        width=1, 
        node_color=["pink" if x in p else "red" if x in r else "yellow" if x in y else "orange" if x in o else "green" if x in g else "magenta" for x in G.nodes()], 
        node_size=150,
        labels=Gend)
plt.title("Grafo Algoritmo Louvain")
plt.show()


#############################
# Ahora hagamos algo parecido pero con Greedy mod

comus = nx.algorithms.community.greedy_modularity_communities(G, weight=None)


# Comus es una lista rara, no me gusta lo de frozenset
# Me armo la lista CD para trabajar mejor

CD=[]

for j in range(len(comus)):
    pin=[]
    for x in comus[j]:
        pin.append(x)
    CD.append(pin)
 
    
# Acá vuelvo a separar los delfines en colores según dominio  
    
for j in range(len(CD)):
    N=len(CD[j])
    for l in range(N):
        LCol[j].append(CD[j][l])
        

nx.draw(G, 
        width=1, 
        node_color=["pink" if x in p else "red" if x in r else "yellow" if x in y else "orange" if x in o else "green" if x in g else "magenta" for x in G.nodes()], 
        node_size=150,
        labels=Gend)
plt.title("Grafo Greedy mod")
plt.show()

