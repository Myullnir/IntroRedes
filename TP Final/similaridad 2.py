import pandas as pd
import time
import geopy
from geopy import distance
import datetime
import networkx as nx
from datetime import datetime, timedelta
df = pd.read_csv(r"C:\Users\Diego\Documents\Diego\Lic. Fisica\Redes Complejas\TC Final\checkins_filtrados_3meses.csv",
                 sep=',', header= 0, index_col=0, 
                 names=['índice', 'nodo', 'fecha', 'latitud', 'longitud', 'ID'])


pd.to_datetime(df[1])
df[1]['año'] = df[1].dt.year 



t0 = time.time()

D = {}
for d in range(5000):## esto para que no me rompa la PC, con ese número  agarra las locations de 16 usuarios X_X
    p = df.iloc[[d]]['nodo'].values[0]
#    print(p)
    lugar = (df.iloc[[d]]['latitud'].values[0],df.iloc[[d]]['longitud'].values[0])
    momento = (df.iloc[[d]]['fecha'].values[0])
    try:
        D[p][lugar] += [momento]
    except:
        try:
            D[p][lugar] = [momento]
        except:
            D[p] = {lugar: [momento]}
print("{}seg".format(time.time()-t0))


a=pd.to_datetime(D[1][(37.63049, -122.411084)])
b=pd.to_datetime(D[2][(39.746396999999995, -104.95976599999999)])
aa = a[0].split(':')
g = aa[0]
f=pd.to_datetime(g)


bb= b.split(':')
l = bb[0]
k=pd.to_datetime(l)
print(f)
print(k)
print(f-k)
print(k<f)


a=D[1].keys()
resta = (f - k).seconds
restaa= resta.seconds

cia = geopy.distance.distance((37.63049, -122.411084), (39.746396999999995, -104.95976599999999)).km

G=nx.read_edgelist(r"C:\Users\Diego\Documents\Diego\Lic. Fisica\Redes Complejas\TC Final\edges_3meses.txt")
vecinos = {n:list(G.neighbors(n)) for n in G.nodes()}

G1 = nx.Graph()
nodos_tomados=[]
for nodo in D.keys():
    nodo=str(nodo)##debe iren G.nodes() pero lo hago aca para qe solo agarre nodos que estan
    nodos_tomados.append(nodo)
    if nodo in vecinos.keys():
        for vecino in vecinos[nodo]:
            if vecino not in nodos_tomados:
                if vecino in D.keys():
                    nodo=int(nodo)
                    vecino=int(vecino)
                    lugares1 = D[nodo].keys()
                    lugares2 = D[vecino].keys()
                    par= nodo, vecino
                    peso_par = 0
                    for lugar1 in lugares1:
                        for lugar2 in lugares2:
                            distancia = distance.distance(lugar1, lugar2).km
                            if distancia < 0.1:
                                for fecha_nodo in D[nodo][lugar1]:
                                    for fecha_vecino in D[vecino][lugar2]:
                                        fechanodo=fecha_nodo.split(':')
                                        fecha1 = pd.to_datetime(fechanodo[0])
                                        fechavecino=fecha_vecino.split(':')
                                        fecha2 = pd.to_datetime(fechavecino[0])
                                        resta = abs((fecha1 - fecha2).seconds)
                                        if resta < 43200000:
                                            peso_par += 1
                    G1.add_edges_from([(nodo, vecino, {'weight': peso_par})])       
                        
                                 
                                 ##ACA HAY QUE CONTAR BIEN QUÉ QUIERO CONTAR
                 
                     
                 
