# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:27:06 2018

@author: Fabio
"""
import numpy as np
import networkx as nx
import matplotlib.pylab as plt
import random
import math
from scipy import optimize

G = nx.read_gml('as-22july06.gml')

Grado=[]


for grad in G.degree:
    Grado.append(G.degree(grad[0]))

Grado.sort()

#for j in range(len(Grado)):
#    print(Grado[j])
    
# # Que necesito para graficar probabilidad?
# #Casos totales
# #print(len(G.degree()))

# #Hasta que k tiene sentido calcular Pk?
# #print(max(Grado))

# #Cuales son los casos favorables? usa el count para eso
# #print(Grado.count(1))

# #Ya estamos, ahora hagamos la probabilidad

Prob=[]

for k in range(1,max(Grado)+1):
    Pk=Grado.count(k)/len(G.degree)
    Prob.append(Pk)

K=np.arange(1,max(Grado)+1)



 # plt.semilogx(K,Prob,"*g")
 # plt.title("Logaritmo en el Eje x, binneado lineal")
 # plt.xlabel("Grado K")
 # plt.ylabel("Probabilidad Pk")
 # plt.show()

 # plt.loglog(K,Prob,"*r")
 # plt.title("Logaritmo en ambos ejes, binneado lineal")
 # plt.xlabel("Grado K")
 # plt.ylabel("Probabilidad Pk")
 # plt.show()


a=np.logspace(0,11,num=12,base=2)
b=2390
Bins=np.append(a,b)
Num=[]
Cen=[]
#plt.hist(Grado,bins=Bins)
Num,Cen=np.histogram(Grado,bins=Bins)


for el,bi in zip(Num,Cen):
    if el==0:
        print(bi)

#Casi estoy, ahora tengo que calcular los Pk Para eso tengo que hacer promedios de los Pk
        
Cenf=Cen.astype(int) #Armo este tipo porque los otros son float.numpy64 y no me los toma

Cent=[] # Es el centro delos bines TRUE

for l in range (len(Cenf)-1):
    m=0
    Long=np.arange(Cenf[l],Cenf[l+1],1)
    for j in Long:
        m=m+(j*(Grado.count(j)))/Num[l]
    m=math.floor(m)
    Cent=np.append(Cent,m)

Cent[len(Cent)-1]=Cen[len(Cen)-1]


Probt=[]

for l in range (len(Cenf)-1):
    m=0
    Long=np.arange(Cenf[l],Cenf[l+1],1)
    for j in Long:
        m=m+Prob[j-1]
    Probt=np.append(Probt,m)

Probt[len(Probt)-1]=Prob[len(Prob)-1]    

#
#plt.loglog(Cent,Probt,"*b")
#plt.title("Logaritmo en ambos, binneado logarítmico en base 2")
#plt.xlabel("Grado K")
#plt.ylabel("Probabilidad de hallar nodo de grado K")
#plt.show()

powerlaw = lambda x, amp, index: amp * (x**index)

logx = np.log10(Cent)
logy = np.log10(Probt)

fitfunc = lambda p, x: p[0] + p[1] * x
errfunc = lambda p, x, y: y-fitfunc(p, x)

pinit = [1.0, 1.0]
out = optimize.leastsq(errfunc, pinit,args=(logx, logy), full_output=1)

pfinal = out[0]
index = pfinal[1]
amp = 10.0**pfinal[0]



plt.loglog(Cent, powerlaw(Cent, amp, index))
plt.loglog(Cent,Probt,"*y")  # Data
plt.xlabel('Grado K')
plt.ylabel('Probabilidad de obtener nodo de Grado K')
