# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 21:26:45 2018

@author: Fabio
"""


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import pandas as pd
import os
import csv
from networkx.algorithms import bipartite

t0=time.time()

def scan(cant,lista):
    i=0
    for x in lista:
        print(x)
        i+=1
        if i>cant:
            break
            
def Tiempo():
    t1=time.time()
    print("Esto tardó {} segundos".format(t1-t0))


def ldata(archive):
        f = open(archive)
        data = []
        for line in f:
            col = line.split("\t")
            col = [x.strip() for x in col]
            data.append(col)
        return data 
    
Amigos=ldata("Brightkite_edges.txt")
#Ubicacion=ldata("Brightkite_totalCheckins.txt")

# Algo que debí definir antes y nunca hice
Maxusu = 0
for x in Amigos:
    Maxusu=max(Maxusu,int(x[0]),int(x[1]))
G = nx.Graph()
G.add_edges_from(Amigos)
Tiempo()
print("Leí los txt")

#--------------------------------------------------------------------------

# os.walk lo que hace es recorrer la carpeta y todas las subcarpetas adentro.
# Root es el path de la carpeta en la que está mirando
# dirs son los nombres de las carpetas dentro de root
# Files son los nombres de todos los archivos dentro de root

# La cosa es que te queda listas dentro de listas. Para cada carpeta que tenga
# Que revisar, va a armar una lista diferente. Así que si le pedís que analice una
# Carpeta con 4 carpetas adentro, te van a quedar en total cinco listas.

# A cada una de estas listas, en la primer coordenada pone el path para entrar a esa carpeta.
# En la segunda coordenada, pone una lista con los nombres de todas las carpetas contenidas
# En la tercer coordenada, pone otra lista con los nombres de todos los archivos contenidos.

CarpCheck=[[root,files] for root,dirs,files in os.walk('Checkins nodo/Checkins Totales/')]

# Como a CarpCheck yo lo hice usando solo root y files, es una lista que se saltea
# Los nombres de las carpetas contenidas


# Nombre de los archivos de Checkins

Labarc= CarpCheck[0][1]


#---------------------------------------------------------------------------

DictID = dict()
DictIDT = dict()
DictLAID = dict()
DictFLAID = dict()

for nombre in Labarc:
    if nombre != "Nodosvacios.csv":
        ListaID = []
        ListaLAID = []
        ListaIDT = []
        ListaFLAID = []
        with open("Checkins nodo/Checkins Totales/{}".format(nombre), newline='') as csvfile:
            # Con el with open abrí mi archivo como csv
            # Con el format voy a recorrer todos los archivos en mi carptea Checkins nodo
            Dat= csv.reader(csvfile, delimiter=',', quotechar='|')
            Data= list(Dat)
            nodo= Data[1][1] # La fila 1 la elegí porque no todos los nodos tienen más de un checkin
            for x in Data[1:]:
                # Me deshago de la isla nula
                if x[5]!="00000000000000000000000000000000":
                    # Le pongo de 1 en adelante porque la primer fila son nombres de columnas
                    if len(x[2])!=0:
                        # Me deshago de los tipos que tienen latitud que no está entre -90 y 90
                        if -90<float(x[3])<90:
                            if x[5] not in ListaID:
                                ListaID.append(x[5])
                                ListaLAID.append([[x[3],x[4]],x[5]])
                            ListaIDT.append(x[5])
                            # Acá armo un Diccionario de fechas
                            dada = x[2].split("T") # Separo en la T, lo de la izquierda es AAAA-MM-DD
                            ListaFLAID.append([dada[0],x[3],x[4],x[5]])
            if len(ListaID)!=0:
                DictIDT[nodo]=ListaIDT
                DictID[nodo]=ListaID
                DictLAID[nodo]=ListaLAID
                DictFLAID[nodo]=ListaFLAID

                

#--------------------------------------------------------------------------------------------

# NCC es Nodos con Check in

NCC=[int(x) for x in DictID.keys()]
NCC.sort()
#
#NotCC=[]
#
#m= 0
#
#for j in range(Maxusu+1):
#    if j!= NCC[j-m]:
#        NotCC.append(j)
#        m +=1
Tiempo()
print("Armé los diccionarios")
#-------------------------------------------------------------------------

# Bueh, al final terminé separándolo todo de nuevo
t0=time.time()

Bip=nx.Graph()
Bip.add_nodes_from(NCC, bipartite = 0, color="orange")

# Con eso agregué todos los usuarios a la red, y les asigne bipartite = 0
for nodo in DictID.keys():
    Bip.add_nodes_from(DictID[nodo], bipartite = 1, color="blue")
# Con eso asigné todos los ID's al grafo, con bipartite = 1.
# De paso, que se repitan no es ningún problema, ya lo comprobé
# Ahora viene lo gede
for nodo in DictID.keys():
    Tuplas = []
    for lugar in DictID[nodo]:
        weight = DictIDT[nodo].count(lugar)
        Tuplas.append((int(nodo),lugar,weight))
    Bip.add_weighted_edges_from(Tuplas)
    
Mam = set(n for n,d in Bip.nodes(data=True) if d['bipartite']==0)
Lugares = set(Bip) - Mam

Lugares=list(Lugares)

Mad = bipartite.biadjacency_matrix(Bip,row_order = NCC, column_order = Lugares)

#-------------------------------------------------------------------------------------------

# Cosas por hacer: Comparar similitudes entre matrices. Para esto, hay tres métodos a mirar:
# 1) Comparar los enlaces formados entre la red de amigos y la red proyectada de usuarios
# 2) Clusterizar la red y luego comparar los grupos para una red 
# y para la otra mediante información mutua
# 3) Lo mismo que para el 2 pero con Precisión

Tiempo()
print("Armé la red bipartita")


#---------------------------------------------------------------------

### Está TODO COMENTADO, La idea es que ya hice todo lo que necesitaba con esto
### No necesito más de esto. Tardaba un montón

## Voy a hacer otro análisis de similaridad ahora
## Voy a querer comparar la similitud de dos personas sobre si van a los mismos lugares
## Y cuantas veces fueron en total
#t0=time.time()
#UI=nx.Graph()
#
## Mad.getnnz me devuelve un array con la cantidad de elementos no nulos en cada fila o columna
## Para columnas tiene que ser un 0 entre paréntesis, para filas tiene que ser un 1.
#
## El i y el j son métodos de control para ver que esté laburando correctamente
## El PV es para ver que el tipo haya hecho la primer pasada
## El mem es para ir ajustando los elementos del array columna a recorrer
#
#
#Filas,Columnas = Mad.nonzero()
#unique,counts = np.unique(Filas,return_counts=True)
#DRangos = dict(zip(unique, counts))
#
#i=0
#fila = 0
#inicio = 0
#fin = DRangos[0]
#Por = np.arange(0,1,0.05)
#v = 0
#
#for nodo1 in NCC[0:1]:
#    LN = []
#    fila += 1
#    ColVis = Columnas[inicio:fin]
#    i1 = NCC.index(nodo1)
#    for columna in ColVis:
#        AN,NI = Mad[:,columna].nonzero() # AN tiene todos los usuarios 
#        # que coinciden en lugares con nodo1. AN es Array de Nodos. NI es No interesa
#        for x in AN:
#            N = NCC[x]
#            if N not in LN:
#                LN.append(N)
#    for nodo2 in LN:
#        i2 = NCC.index(nodo2)
#        INT = 0
#        UNI = 0
#        # LL es la lista de lugares a recorrer
#        LL = set(DictID[str(nodo1)]).intersection(set(DictID[str(nodo2)]))
#        i += 1
#        for place in LL:
#            lugar = Lugares.index(place)
#            inter = min(Mad[i1,lugar],Mad[i2,lugar])
#            INT += inter
#        LT = set(DictID[str(nodo1)]).union(set(DictID[str(nodo2)]))
#        # LT es la lista de Lugares Totales
#        for place in LT:
#            uni = max(DictIDT[str(nodo1)].count(place),DictIDT[str(nodo2)].count(place))
#            UNI += uni
#        Similaridad=INT/UNI
#        if Similaridad>0.005:
#            UI.add_edge(nodo1,nodo2,Simil = Similaridad)
#    inicio += DRangos[fila]
#    fin += DRangos[fila]
##     fR = nodo1/len(NCC)
##     if fR>Por[v]:
##         print("Ya terminé el {} porciento".format(Por[v]*100))
##         Tiempo()
##         v += 1
#    
#    
#    
#    
#
## Me tardó 390, eso no es tanto
#
#print("i es:",i)
#print("i debería ser 1695220878")
#print(len(UI.edges()))
#
## Una vez armado el grafo, empiezo a armarme mi espaciado de similaridades para ver cómo
## Va a variar el procentaje de overlap entre enlaces a medida que vuevlo más estricto el
## Criterio de similaridad
#
## PV = False #Esto es para registrar si es el primer elemento del for
#
## for x in nx.get_edge_attributes(UI,"Simil").values():
##     if PV==False:
##         maxS = x
##         minS = x
##         PV = True
##     maxS = max(maxS,x)
##     minS = min(minS,x)
#    
## print(maxS)
## print(minS)
#
## HAL = UI.copy()
#
## X = linspace(minS,maxS,10)
#
## LEnlaG = [[int(x[0]),int(x[1])] for x in G.edges()]
## for i in range(len(LEnlaG)):
##     if LEnlaG[i][0]>=LEnlaG[i][1]:
##             LEnlaG[i]=[LEnlaG[i][1],LEnlaG[i][0]]
## LEnlaG.sort(key=lambda x: x[0])
#
## for simil in X:
##     for tupla in nx.get_edge_attributes(HAL,"Simil").items():
##         if tupla[1]<simil:
##             HAL.remove_edge(tupla[0])
##     LEnlaUI = []
##     LEnlaUI = [[int(x[0]),int(x[1])] for x in UI.edges()]
##     # Una vez armada la lista, la ordeno para que quede el usuario 
##     # Con número menor a la izquierda siempre
##     for i in range(len(LEnlaUI)):
##         if LEnlaUI[i][0]>=LEnlaUI[i][1]:
##             LEnlaUI[i]=[LEnlaUI[i][1],LEnlaUI[i][0]]
##     LEnlaUI.sort(key=lambda x: x[0])
##     Rangos = []
##     # inicio es como el ret en su momento. A cada iteracion me marca
##     # Cuantas filas de cada nodo encontro, y luego empieza justo en la primera del siguiente nodo
##     inicio = 0
##     n=1
##     for nodo in NCC:
##         Rangos.append([inicio,0])
##         for enlace in LEnlaUI[inicio:inicio+15000]:
##             if enlace[0]!=nodo:
##                 break
##             inicio += 1
##         Rangos[nodo][1] = inicio
##         if nodo>n*5000:
##             print("Estoy trabajando amo, ya hice hasta el nodo",nodo)
##             n += 1
##     fracen=0
##     Den=len(UI.edges())
##     for enlace1 in LEnlaG:
##         for enlace2 in LEnlaUI[Rangos[enlace1[0]][0]:Rangos[enlace1[0]][1]]:
##             if enlace1==enlace2:
##                 fracen += 1/Den
##                 break
##     print("La fracción de enlaces del segundo grafo que se repiten en el primer grafo es:",fracen)

#-----------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

# Hagamos el gráfico de distancia máxima en función del grado
from geopy.distance import lonlat, distance
t0=time.time()
LNLAID = [] #Lista con la ubicación más visitada de cada nodo
for nodo in DictID.keys():
    Maxim = 0
    LQV = len(DictID[nodo])
    if LQV>1:
        for lugar in DictID[nodo]:
            weight = DictIDT[nodo].count(lugar)
            Maxim = max(Maxim,weight)
            if Maxim==weight:
                Lugar=lugar #De esta manera, Lugar es el más visitado de cada nodo
        for fila in DictLAID[nodo]:
            if fila[1]==Lugar: #Así me aseguro de tener la data del ID correspondiente
                Lat=fila[0][0]
                Alt=fila[0][1] #Con esto consigo los datos de latitud y altitud
                break
        LNLAID.append([nodo,float(Lat),float(Alt),Lugar])

# Ya tengo el lugar más visitado de cada persona. Necesito ahora la distancia máxima de cada persona
# Ya que puedo, intento calcular la cantidad de lugares visitados, que no es lo mismo que 
# cantidad de Check-Ins
Reg=[] #Registro de datos
for fila in LNLAID:
#     print("Estoy mirando el nodo:",fila[0])
    maxd = 0
    for LAID in DictLAID[fila[0]]:
#       print("Las coordenadas de Lat y Alt del hogar son:", fila[1],fila[2])
#       print("Las coordenadas de Lat y Alt a comparar son:", LAID[0][0],LAID[0][1])
        lugarh = (fila[2],fila[1])
        lugar2 = (float(LAID[0][1]),float(LAID[0][0]))
        distancia = distance(lonlat(*lugarh), lonlat(*lugar2)).km
        maxd = max(distancia,maxd)
    LQV = len(DictID[fila[0]])
    Reg.append([maxd,LQV])
        
DMax = [x[0] for x in Reg]
LugVis = [x[1] for x in Reg]

# Ahora, para graficarlo es un tema, porque de seguro la cantidad de LugVis se va repitiendo
X = []
Y = []
for j in range(min(LugVis),max(LugVis)+1):
    LPro = []
    for num,dist in zip (LugVis,DMax):
        if j==num:
            LPro.append(dist)
    if len(LPro)!=0:
        dpro=np.mean(LPro)
        X.append(j)
        Y.append(dpro)

plt.figure()
plt.semilogx(X,Y,"o")
plt.grid()
plt.title("Distancia máxima Vs Cantidad de lugares visitados")
plt.xlabel("Cantidad de lugares visitados")
plt.ylabel("Distancia Máxima (Km)")
plt.show()
            
            
Tiempo()      

#---------------------------------------------------------------------------
# Voy a juntar acá a los histogramas

# Distribuciòn de cantidad de localidades distintas visitadas

import math
Histo=[]
for x in DictID.values():
    Histo.append(len(x))
Bin=math.floor(max(Histo)/10)

plt.figure()
plt.hist(Histo,bins=Bin,log=True)
plt.rcParams.update({'font.size': 10})
plt.grid()
plt.title("Distribución de cantidad de lugares distintos visitados")
plt.show()
#-----------------------------------------------------------------
# Ahora hagamos distribuciòn de grado
Grado=[]
for x in G.degree():
    Grado.append(x[1])
A= np.mean(Grado)
Bin=math.floor(max(Grado)/10)

plt.figure()
plt.hist(Grado,bins=Bin,log=True)
plt.rcParams.update({'font.size': 14})
plt.title("Distribución de grado")
plt.grid()
plt.show()

#-----------------------------------------------------------------------

# Debería hacer una relación entre distribución de grado Cantidad de ID's visitados
t0=time.time()
# Me armo un diccionario de grado para cada nodo
DictGrado = dict()
Gradmax=0
for x in G.degree():
    DictGrado[x[0]]=x[1]
    Gradmax=max(Gradmax,x[1])
Lgrados= list(set(Grado))
Lgrados.sort()
X=[]
Y=[]
# Este método tarda mucho, busquemos otra forma de armar el gráfico
# for grad in Lgrados:
#     LPromed = []
#     for pareja in DictGrado.items():
#         if pareja[0] in NCC and pareja[1]==grad:
#             LPromed.append(len(DictID[pareja[0]]))
#         if pareja[0] not in NCC and pareja[1]==grad:
#             LPromed.append(0)
#     Promed=np.mean(LPromed)
#     X.append(grad)
#     Y.append(Promed)
    
    
#--------------------------------------------------------

# GradID = []

# for nodo in NCC:
#     GradID.append([nodo,DictGrad[nodo],len(DictID[nodo])])

# # Ya me armé la lista de grado e ID, la sorteo según grado
# GradID.sort(key=lambda x:x[1])

#--------------------------------------------------------------

DictGID = dict()
# DictGID es un diccionario que a cada grado le va a asignar una lista con 
# la cantidad de ID's distintos visitados por cada usuario.
# Pero no guarda registro de cuales nodos son los que tenían ese grado o ese ID
for grad in Lgrados:
    DictGID[grad]=[]
for tupla in G.degree():
    if int(tupla[0]) in NCC:
        DictGID[tupla[1]].append(len(DictID[tupla[0]]))
    else:
        DictGID[tupla[1]].append(0)
# Lo siguiente me arma mis listas X e Y con los valores a plotear, asignándolos de manera
# Correspondiente a los valores en X e Y. Espero que el hecho de que no estén ordenados no
# sea un problema     
for pareja in DictGID.items():
    x=pareja[0]
    y=np.mean(pareja[1])
    X.append(x)
    Y.append(y)
Tiempo()
# plt.plot(X,Y)
# plt.grid()
# plt.xlabel("Grado")
# plt.ylabel("Cantidad de ID's distintas")
# plt.title("Cantidad de ID's en función del grado")
# plt.show()

#---------------------------------------------------------

# Ahora hagámoslo sin contar los tipos con 0 Checkins
for grad in Lgrados:
    DictGID[grad]=[]
for tupla in G.degree():
    if int(tupla[0]) in NCC:
        DictGID[tupla[1]].append(len(DictID[tupla[0]]))
# Lo siguiente me arma mis listas X e Y con los valores a plotear, asignándolos de manera
# Correspondiente a los valores en X e Y. Espero que el hecho de que no estén ordenados no
# sea un problema
X=[]
Y=[]    
for pareja in DictGID.items():
    if len(pareja[1])!=0:
        x=pareja[0]
        y=np.mean(pareja[1])
        X.append(x)
        Y.append(y)

Tiempo()

plt.figure()      
plt.loglog(X,Y,"or")
plt.grid()
plt.xlabel("Grado")
plt.ylabel("Cantidad de ID's distintas")
plt.title("Cantidad de ID's en función del grado")
plt.show()
#--------------------------------------------------------------------
# Por último, hagámoslo para el largo total de los ID's
for grad in Lgrados:
    DictGID[grad]=[]
for tupla in G.degree():
    if int(tupla[0]) in NCC:
        DictGID[tupla[1]].append(len(DictIDT[tupla[0]]))
    else:
        DictGID[tupla[1]].append(0)
# Lo siguiente me arma mis listas X e Y con los valores a plotear, asignándolos de manera
# Correspondiente a los valores en X e Y. Espero que el hecho de que no estén ordenados no
# sea un problema
X=[]
Y=[]  
for pareja in DictGID.items():
    x=pareja[0]
    y=np.mean(pareja[1])
    X.append(x)
    Y.append(y)

        
Tiempo()
        
# plt.loglog(X,Y,"orange")
# plt.grid()
# plt.xlabel("Grado")
# plt.ylabel("Cantidad de Check-ins")
# plt.title("Cantidad de Check-Ins en función del grado")
# plt.show()

#----------------------------------------------------------------------
# Por último último, hagámoslo sin contar los vacíos de check-ins
# Para cantidad total de Check-ins
for grad in Lgrados:
    DictGID[grad]=[]
for tupla in G.degree():
    if int(tupla[0]) in NCC:
        DictGID[tupla[1]].append(len(DictIDT[tupla[0]]))
# Lo siguiente me arma mis listas X e Y con los valores a plotear, asignándolos de manera
# Correspondiente a los valores en X e Y. Espero que el hecho de que no estén ordenados no
# sea un problema
X=[]
Y=[]  
for pareja in DictGID.items():
    if len(pareja[1])!=0:
        x=pareja[0]
        y=np.mean(pareja[1])
        X.append(x)
        Y.append(y)     
Tiempo()

# le voy a cambiar el binneado al gráfico, no va a ser logarítmico
X2 = []
for i in range(200):
    if math.floor(1.4**i)>X[len(X)-1]:
        break
    X2.append(math.floor(1.4**i))
X2.append(X[len(X)-1])
X2 = set(X2)
X2 = list(X2)
X2.sort()
print(len(X2))

Y2 = []
for j in range(len(X2)-1):
    for x in X:
        if X2[j]<x<X2[j+1]:
            
            


plt.figure()        
plt.loglog(X,Y,"og")
plt.grid()
plt.xlabel("Grado")
plt.ylabel("Cantidad de Check-ins")
plt.title("Cantidad de Check-Ins en función del grado")
plt.show()

