import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from random import randint
#c)
##Ahora utilizo los observables topológicos GRADO, COEF CLUSTERING

def ldata(archive):
        f=open(archive)
        data=[]
        for line in f:
            line=line.strip()
            col=line.split()
            data.append(col)	
        return data
    
sexos_reales=ldata("dolphinsGender.txt")
##grafo real y grafo copia
G_real=nx.read_gml("D:\Mis Documentos\Diego\LICENCIATURA EN FISICA - DIEGO\Redes Complejas\TC01\dolphins.gml")
G_real1=nx.read_gml("D:\Mis Documentos\Diego\LICENCIATURA EN FISICA - DIEGO\Redes Complejas\TC01\dolphins.gml")
for sexo in sexos_reales:
    G_real.node[sexo[0]]["genero"]=sexo[1]
for sexo in sexos_reales:
    G_real1.node[sexo[0]]["genero"]=sexo[1] 


diametro=[]
diametro1=[]
diametro2=[]
lista_nodos=list(G_real.nodes())
pasos=[i for i in range(len(lista_nodos)-1)]


clustering_list1=[]
grado_list1=[]

pasos_doble_comp_gigante=[]
promedio_doble_comp_gigante=[]

#Función que asigna a los nodos un observable dado
def asignador_nodos_observable(observable_dict, observable_string):    
    for observable in observable_dict:
        G_real1.node[observable[0]][observable_string]=observable[1]
    for observable in observable_dict:
        G_real.node[observable[0]][observable_string]=observable[1]                    
                    
#Función que remueve nodos dado un observable, calcula el diametro de la componente gigante y de las dos componentes conexas
#más grandes del grafo, guarda eso y la cantidad de pasos (cada nodo removido) en listas
def removedor_nodos_observable(observable_lista, observable_string):
    for observable in observable_lista:
        for nodo in G_real1.nodes():
            if G_real1.node()[nodo][observable_string]==observable:
                G_real.remove_node(nodo)
                if len(G_real)>=1:
                    todas_comps_gigantes=list(nx.connected_component_subgraphs(G_real))
                    todas_comps_gigantes.sort(key=len, reverse=1)
                    CG=max(nx.connected_component_subgraphs(G_real), key=len)
                    DCG=nx.diameter(CG)
                    diametro.append(DCG)
                    if len(todas_comps_gigantes) > 1:
                            comp1=todas_comps_gigantes[0]
                            comp2=todas_comps_gigantes[1]
                            DCG1=nx.diameter(comp1)
                            DCG2=nx.diameter(comp2)
                            diametro1.append(DCG1)
                            diametro2.append(DCG2)
                    else:
                        comp1=todas_comps_gigantes[0]
                        DCG1=nx.diameter(comp1)
                        diametro1.append(DCG1)
                        diametro2.append(DCG1)
                        
                        

                            
                            
#Función que dada una lista remueve nodos aleatoriamente y guarda los valores de las las dos componentes conexas
#más grandes del grafo (en caso de que las hubiera), le calcula
#el diámetro a cada una y guarda el número de pasos
def removedor_aleatorio_diametro_pasos(lista_nodos):
    random.shuffle(lista_nodos)
    for nodo in lista_nodos:
        G_real.remove_node(nodo)
        if len(G_real)>=1:
            todas_comps_gigantes=list(nx.connected_component_subgraphs(G_real))
            todas_comps_gigantes.sort(key=len, reverse=1)
            if len(todas_comps_gigantes) > 1:
                    comp1=todas_comps_gigantes[0]
                    comp2=todas_comps_gigantes[1]
                    DCG1=nx.diameter(comp1)
                    DCG2=nx.diameter(comp2)
                    diametro1.append(DCG1)
                    diametro2.append(DCG2)
            else:
                        comp1=todas_comps_gigantes[0]
                        DCG1=nx.diameter(comp1)
                        diametro1.append(DCG1)
                        diametro2.append(DCG1)
                            
                            
#Funciones para hallar en qué momento las dos componentes más grandes tiene diámetros similares (tomando como criterio si están separados en 1)
#y cuánto es el promedio entre ambos diámetros
def hallar_doble_comp_gigante(pasos, diametro1, diametro2):
    for paso,d1,d2 in zip(pasos, diametro1, diametro2):
        if abs(d1-d2)==2 and d1!=0:
            return paso

def hallar_doble_comp_gigante2(pasos, diametro1, diametro2):
    for paso,d1,d2 in zip(pasos, diametro1, diametro2):
        if abs(d1-d2)==2 and d1!=0:
            return (d1+d2)/2



#Clustering de cada nodo +
#Armo listas de valores de clustering, de grado
clustering_dict=nx.clustering(G_real)
clustering_dict_items=clustering_dict.items()
clustering_list=list(clustering_dict.values())
clustering_list.sort()

grado_dict=dict(nx.degree(G_real))
grado_dict_items=grado_dict.items()
grado_list=list(grado_dict.values())
grado_list.sort()




## Armo un listas sólo con los coef de clustering y grados que no se repiten, las ordeno de Mayor a menor(Mam) y de menor a Mayor (maM)
#son las que voy a usar para quitar nodos dado el orden y la variable
for i in clustering_list:
    if i not in clustering_list1:
        clustering_list1.append(i)
clustering_list1_Mam=sorted(clustering_list1, reverse=1)
clustering_list1_maM=sorted(clustering_list1, reverse=0)


for i in grado_list:
    if i not in grado_list1:
        grado_list1.append(i)
grado_list1_Mam=sorted(grado_list1, reverse=1)
grado_list1_maM=sorted(grado_list1, reverse=0)


#Hasta acá hay que correr todo normal, para ver el comportamiento de la red eliminando según grafo o clústering y de mayor a menor o menor a mayor
#hay que correr uno por uno los BLOQUES siguientes, reasignando las variables antes de cada corrida de BLOQUE

#
###---------------------------------------------------BLOQUE-------------------------------------------------
##Elimino de Mayor a menor clustering
lista_nodos=list(G_real.nodes())
asignador_nodos_observable(grado_dict_items, "grado")
removedor_nodos_observable(grado_list1_Mam, "grado")
hallar_doble_comp_gigante(pasos, diametro1, diametro2)
hallar_doble_comp_gigante2(pasos, diametro1, diametro2)
print("Eliminando nodos de Mayor a menor grado se llega a dos componentes gigantes de tamaños similares a los ", hallar_doble_comp_gigante(pasos, diametro1, diametro2)+1, "pasos")
print("El diámetro promedio de ambas componentes es", hallar_doble_comp_gigante2(pasos, diametro1, diametro2))
plt.xlabel("Pasos")
plt.ylabel("Diámetro componente gigante")
plt.plot(pasos, diametro1, label='Diámetro 1° componente conexa')
plt.plot(pasos, diametro2, label='Diámetro 2° componente conexa')
plt.legend()
plt.show()
##---------------------------------------------------BLOQUE-------------------------------------------------

##Elimino de menor a Mayor clustering
lista_nodos=list(G_real.nodes())
asignador_nodos_observable(grado_dict_items, "grado")
removedor_nodos_observable(grado_list1_maM, "grado")
hallar_doble_comp_gigante(pasos, diametro1, diametro2)
hallar_doble_comp_gigante2(pasos, diametro1, diametro2)
print("Eliminando nodos de menor a mayor grado se llega a dos componentes gigantes de tamaños similares a los ", hallar_doble_comp_gigante(pasos, diametro1, diametro2), "pasos")
print("El diámetro promedio de ambas componentes es", hallar_doble_comp_gigante2(pasos, diametro1, diametro2))
plt.xlabel("Pasos")
plt.ylabel("Diámetro componente gigante")
plt.plot(pasos, diametro1, label='Diámetro 1° componente conexa')
plt.plot(pasos, diametro2, label='Diámetro 2° componente conexa')
plt.legend()
plt.show()
##---------------------------------------------------BLOQUE-------------------------------------------------

##Elimino nodos de Mayor a menor grado
lista_nodos=list(G_real.nodes())
asignador_nodos_observable(clustering_dict_items, "clustering")
removedor_nodos_observable(clustering_list1_Mam, "clustering")
hallar_doble_comp_gigante(pasos, diametro1, diametro2)
hallar_doble_comp_gigante2(pasos, diametro1, diametro2)
print("Eliminando nodos de Mayor a menor clustering se se llega a dos componentes gigantes de tamaños similares a los ", hallar_doble_comp_gigante(pasos, diametro1, diametro2), "pasos")
print("El diámetro promedio de ambas componentes es", hallar_doble_comp_gigante2(pasos, diametro1, diametro2))
plt.xlabel("Pasos")
plt.ylabel("Diámetro componente gigante")
plt.plot(pasos, diametro1, label='Diámetro 1° componente conexa')
plt.plot(pasos, diametro2,  label='Diámetro 2° componente conexa')
plt.legend()
plt.show()
##---------------------------------------------------BLOQUE-------------------------------------------------

##Elimino nodos de menor a Mayor grado
lista_nodos=list(G_real.nodes())
asignador_nodos_observable(clustering_dict_items, "clustering")
removedor_nodos_observable(clustering_list1_maM, "clustering")
hallar_doble_comp_gigante(pasos, diametro1, diametro2)
hallar_doble_comp_gigante2(pasos, diametro1, diametro2)
print("Eliminando nodos de menor a mayor clustering se llega a dos componentes gigantes de tamaños similares a los ", hallar_doble_comp_gigante(pasos, diametro1, diametro2), "pasos")
print("El diámetro promedio de ambas componentes es", hallar_doble_comp_gigante2(pasos, diametro1, diametro2))
plt.xlabel("Pasos")
plt.ylabel("Diámetro componente gigante")
plt.plot(pasos, diametro1, label='Diámetro 1° componente conexa')
plt.plot(pasos, diametro2, label='Diámetro 2° componente conexa')
plt.legend()
plt.show()

#--------------------------------------------------------------------------------------------------
#Ahora voy a eliminar nodos aleatoriamente:





##Con esto puedo ver los gráficos del diámetro de las componentes gigantes en función del número de nodos(pasos) eliminados para una corrida
#plt.plot(pasos, diametro1)
#plt.show()
#plt.plot(pasos, diametro2)
#plt.show()

#------------------------------------------------
#Armo dos listas e itero mil veces la secuencia generar grafo + remover nodos aleatoriamente + ver en qué paso se empezaron a parecer
#una lista es la cantidad de pasos en los que se llegó a componentes gigantes parecidas para cada iteración
#la otra con el promedio de ambas componentes gigantes para cada iteración

#Para correr ésto último hay que hacer las asignaciones de nuevo, igual que en los BLOQUES

pasos_doble_comp_gigante=[]
promedio_doble_comp_gigante=[]
for i in range(1000):
    G_real=nx.read_gml("dolphins.gml")
    lista_nodos=list(G_real.nodes())
    diametro1=[]
    diametro2=[]
    removedor_aleatorio_diametro_pasos(lista_nodos)
    hallar_doble_comp_gigante(pasos, diametro1, diametro2)
    hallar_doble_comp_gigante2(pasos, diametro1, diametro2)
    pasos_doble_comp_gigante.append(hallar_doble_comp_gigante(pasos, diametro1, diametro2))
    promedio_doble_comp_gigante.append(hallar_doble_comp_gigante2(pasos, diametro1, diametro2))
    
    
#print(pasos_doble_comp_gigante)
#print(np.mean(promedio_doble_comp_gigante))






##Quito los none que puedan aparecer
pasos_doble_comp_gigante=[x for x in pasos_doble_comp_gigante if x is not None]

#Cuento cuantas veces en las iteraciones se repitió un número de pasos tal que se logren dos componentes gigantes parecidas:
#recorro la lista obtenida en la iteración anterior(pasos_doble_comp_gigante) a la que le cuento cuántas veces aparece cada valor y con ellos 
#armo una nueva lista(veces_de_pasos_doble_comp) que va del mínimo al máximo. 
veces_de_pasos_doble_comp=[]
for j in range(min(pasos_doble_comp_gigante), max(pasos_doble_comp_gigante),1):
    veces_de_pasos_doble_comp.append(pasos_doble_comp_gigante.count(j))

#Armo un rango con todos los posibles pasos en los que se obtuvieron las componentes gigantes similares, la idea respecto de lo hecho antes es que tengan
#la misma longitud para armar el histograma

rango=[]
for j in range(min(pasos_doble_comp_gigante), max(pasos_doble_comp_gigante),1):
    rango.append(j)
    
#Histograma de cantidad de veces en función del número de pasos para los cuales se llegó a componentes conexas de diámetros parecidos
plt.bar(rango,veces_de_pasos_doble_comp)
plt.axvline(28, c="red", label='Grado Secuencia-Mam') #Grado - Mam
plt.axvline(46, c="green", label='Grado Secuencia-maM') #Grado - maM
plt.axvline(41, c="blue", label='Clústering Secuencia-Mam') #Clustering - Mam
plt.axvline(32, c="pink", label='Clústering Secuencia-maM') #Clustering - maM
plt.ylabel("Repeticiones")
plt.xlabel("Cantidad de pasos para obtener dos componentes similares")
plt.legend()
plt.show()






  
