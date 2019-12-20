#Quiero que este codigo haga lo mismo que analisis.cpp
#usando pandas, para ver si el ahorro de tiempo es considerable
import pandas as pd
import time

t0 = time.time()
df = pd.read_csv('Brightkite_totalCheckins.txt',sep='\t',header=None)
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

personas = #?
latitud = df[2].values
longitud = df[3].values
tiempos = df[1].values

#D[p] = {lugar1: cant1, lugar2: cant2, lugar3: cant3,...}
D = {}
for d in range(len(df)):
    p = df.iloc[[d]][0].values[0]
    lugar = (df.iloc[[d]][2].values[0],df.iloc[[d]][3].values[0])
    try:
        D[p][lugar] += 1
    except:
        try:
            D[p][lugar] = 1
        except:
            D[p] = {lugar: 1}

#para el nodo 0:
L = list(D[0].items())
L.sort(key=lambda x:x[1])
L[-2]


coordenadas = zip(latitud,longitud)
lugares = set(coordenadas)
for p in personas:
    

