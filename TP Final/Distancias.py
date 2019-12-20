#Quiero que este codigo haga lo mismo que analisis.cpp
#usando pandas, para ver si el ahorro de tiempo es considerable
import pandas as pd
import time
import numpy as np

t0 = time.time()
df = pd.read_csv(r"D:\Mis Documentos\Diego\LICENCIATURA EN FISICA - DIEGO\Redes Complejas\TC final\Brightkite_totalCheckins.txt",sep='\t',header=None)
#print('Tarda {} segundos en hacer el dataframe'.format(time.time()-t0))

header = [2,3]
df.to_csv('checkins_places.csv', columns = header)
print('{} seg'.format(time.time()-t0))
# En la compu rapida del df tarda 26 seg

# Primero, agarramos los lugares
# Nos preguntamos quienes van ahi
# Para c/persona que fue ahi, nos fijamos la frecuenia de la visita (semanal, etc)
# Si esa frecuancia supera cierto umbral, y es periodica semanalmente, diremos que es un lugar de trabajo para esa persona

# OTRA IDEA: tomamos a cada persona, y tomamos los dos lugares que mas frecuentan
#  Los lugares de trabajpo seran aquellos que aparezcan mas veces en los pares mas freceuentados de lugares, de personas

latitud = df[2].values
longitud = df[3].values
tiempos = df[1].values

ta=time.time()
#D[p] = {lugar1: cant1, lugar2: cant2, lugar3: cant3,...}
D = {}
for d in range(len(df)-4730000):## esto para que no me rompa la PC, con ese número  agarra las locations de 16 usuarios X_X
    p = df.iloc[[d]][0].values[0]
    lugar = (df.iloc[[d]][2].values[0],df.iloc[[d]][3].values[0])
    try:
        D[p][lugar] += 1
    except:
        try:
            D[p][lugar] = 1
        except:
            D[p] = {lugar: 1}
print('{} segundos'.format(time.time()-ta))
            
np.save('Diccionario_D.npy', D)

D=np.load('Diccionario_D.npy').item()
D1=np.load('Diccionario_D.npy').item()


for nodo in range(16):
    items=D[nodo].items()
    items_nuevos = sorted(items, key = lambda x: x[1], reverse=True)
    D[nodo]=items_nuevos

# # Quiero ver las distancias entre los 3 primeros lugares visitados:

import geopy
from geopy import distance


distancias_max_nodo  = []
distancias_promedio_nodo = []

for nodo in range(16):##aca tiene que ir for nodo in G.nodes()
        ##tomo los tres primeras lotacions mas visitadas
        a=D[nodo][0][0]
        b=D[nodo][1][0]
        c=D[nodo][2][0]
        d_max = distance.distance(a, c).km
        distancias_max_nodo.append([nodo, d_max])
        d_ab = distance.distance(a, b).km
        d_bc  = distance.distance(b, c).km
        d_ac = distance.distance(a, c).km
        prom=[int(d_ab), int(d_ac)]
        d_prom=np.mean(prom)
        distancias_promedio_nodo.append([nodo, d_prom])
        
        
# a=(39.00000, 104.000000)
# b=(38.00000, 104.000000)
# c=distance.distance(a, b).km
# print(c)


# j=(39.000000, 104.000000)
# k=(39.000000, 105.000000)
# l=distance.distance(j,k).km
# print(l)
# d=round(a[0], 2)
# print(a[0])
# print(d)
# e=distance.distance(39.020000, 39.015555).km
# print(e)
# print(b[0])


