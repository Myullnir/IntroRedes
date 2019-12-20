import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from random import randint
import collections
from collections import OrderedDict

def ldata(archive):
        f=open(archive)
        data=[]
        for line in f:
            line=line.strip()
            col=line.split()
            data.append(col)	
        return data
    
sexos_reales=ldata("dolphinsGender.txt")
sexos_azar=ldata("dolphinsGender.txt")

G_real=nx.read_gml("dolphins.gml")
G_azar=nx.read_gml("dolphins.gml")

##Asigno  géneros a ambos grafos
for sexo in sexos_reales:
    G_real.node[sexo[0]]["genero"]=sexo[1]
for sexo in sexos_azar:
    G_azar.node[sexo[0]]["genero"]=sexo[1]
    

##asignacion aleatoria de generos conservando las cantidades de m, f, y NA iniciales
def aleatorizador_sexos(sexos_azar):
    sexos_aleatorios=[]
    for delfines in sexos_azar:
        sexos_aleatorios.append(delfines[1])
        random.shuffle(sexos_aleatorios)
    for sexo,i in zip(sexos_reales, sexos_aleatorios):
        G_azar.node[sexo[0]]["genero"]=i

#cuento cuántos enlaces intragénero hay dada una aleatorización de géneros

def contador_de_enlaces_ig_azar():
    cuantos=[]
    for enlaces in G_azar.edges():
        g1=G_azar.node[enlaces[0]]["genero"]
        g2=G_azar.node[enlaces[1]]["genero"]
        if g1==g2:
            cuantos.append(g1)
            masculinos=cuantos.count("m")
            femeninos=cuantos.count("f")
            NAs=cuantos.count("NA")
    enlaces_totales_ig_azar=len(cuantos)
#    print(cuantos)
#    print("enlaces entre nodos m",masculinos)
#    print("enlaces entre nodos f", femeninos)
#    print("enlaces entre nodos NA", NAs)
#    print("enlaces totales intragenero_azar", len(cuantos))
    return (enlaces_totales_ig_azar)



def contador_de_enlaces_eg_azar():
    cuantos_eg=[]
    for enlaces in G_azar.edges():
        g1=G_azar.node[enlaces[0]]["genero"]
        g2=G_azar.node[enlaces[1]]["genero"]
        if g1!=g2:
            cuantos_eg.append(g1)
    enlaces_totales_eg_azar=len(cuantos_eg)
    return(enlaces_totales_eg_azar)

#verificación la cantidad de enlaces totales debe ser la suma de los intragenero y los extragenero
#print(len(G_azar.edges()))
#contador_de_enlaces_ig_azar()
#contador_de_enlaces_eg_azar()


##repito mil veces la aleatorización de géneros y veo cuántos enlaces intragénero hubo en cada corrida
    
cantidades_de_enlaces_ig_azar=[]
for i in range(10000):
    aleatorizador_sexos(sexos_azar)
    cantidades_de_enlaces_ig_azar.append(contador_de_enlaces_ig_azar())
   
    

#recorro los valores posibles de enlaces intragénero y digo en qué cantidad de las 1000 iteraciones hubieron esa cantidad de enlaces

enlaces_ig_iteracion_azar=[] 
##lista de la cantidad de veces que ocurrieron K-enlaces intragénero y tambien K es índice de la lista
for j in range(min(cantidades_de_enlaces_ig_azar), max(cantidades_de_enlaces_ig_azar),1):
    enlaces_ig_iteracion_azar.append(cantidades_de_enlaces_ig_azar.count(j))

rango=[]
for j in range(min(cantidades_de_enlaces_ig_azar), max(cantidades_de_enlaces_ig_azar),1):
    rango.append(j)


def contador_de_enlaces_ig_real():
    cuantos=[]
    for enlaces in G_real.edges():
        g1=G_real.node[enlaces[0]]["genero"]
        g2=G_real.node[enlaces[1]]["genero"]
        if g1==g2:
            cuantos.append(g1)
            masculinos=cuantos.count("m")
            femeninos=cuantos.count("f")
            NAs=cuantos.count("NA")
    enlaces_totales_ig_real=len(cuantos)
#    print(cuantos)
    print("enlaces entre nodos m",masculinos)
    print("enlaces entre nodos f", femeninos)
    print("enlaces entre nodos NA", NAs)
    print("enlaces totales intragenero_real", len(cuantos))
    return (enlaces_totales_ig_real)



def contador_de_enlaces_eg_real():
    cuantos_eg=[]
    for enlaces in G_real.edges():
        g1=G_real.node[enlaces[0]]["genero"]
        g2=G_real.node[enlaces[1]]["genero"]
        if g1!=g2:
            cuantos_eg.append(g1)
    enlaces_totales_eg_real=len(cuantos_eg)
    return(enlaces_totales_eg_real)
    
enlaces_ig_real=contador_de_enlaces_ig_real()


print("Hipótesis nula para enlaces intragénero")
plt.bar(rango,enlaces_ig_iteracion_azar)
plt.axvline(enlaces_ig_real, c="red")
plt.legend(['Enlaces intragénero reales'])
plt.ylabel("Repeticiones")
plt.xlabel("Cantidad de enlaces intragénero")
plt.show()

print("el máximo número de enlaces intragénero dada una distribución aleatoria de géneros es:", max(cantidades_de_enlaces_ig_azar))
print("el máximo número de enlaces intragénero dada una distribución aleatoria de géneros es:", min(cantidades_de_enlaces_ig_azar))


##cantidad de enlaces intragenero de la red original



print("la cantidad de enlaces intragénero en la red real es:", contador_de_enlaces_ig_real() )
#p-value

pv=(max(cantidades_de_enlaces_ig_azar)-enlaces_ig_real)/(max(cantidades_de_enlaces_ig_azar)-min(cantidades_de_enlaces_ig_azar))
print("el valor del p-value es", pv)



## 1)Valor medio de enlaces IG y eror para la distribucion al azar
## 2)Lo comparo con el valor esperado, segun el modelo, de la red real

##1)

print("el valor medio de enlaces intragenero para la distribucion al azar es:", np.mean(cantidades_de_enlaces_ig_azar))






enlaces_posibles=0
for nodo1 in G_real.degree():
    for nodo2 in G_real.degree():
        if G_real.node[nodo1[0]]["genero"]==G_real.node[nodo2[0]]["genero"]:
            enlaces_posibles = enlaces_posibles + (nodo1[1]*nodo2[1])
enlaces_posibles = enlaces_posibles/float(4*len(G_real.edges()))

print("Dada la distribución de grados de cada nodo, la cantidad de enlaces intragénero esperada es:", enlaces_posibles)







