import pandas as pd
import time
import numpy as np

df = pd.read_csv('loc-brightkite_totalCheckins.txt',sep='\t',header=None)
#print('Tarda {} segundos en hacer el dataframe'.format(time.time()-t0))

# De alguna forma tenemos que definir un orden para los
# tiempos, que tienen la forma '2010-10-17T01:48:53Z'

# numb('2010-10-17T01:48:53Z') = 20101017014853
def numb(s):
    return int(s.replace('-','').replace(':','').replace('T','').replace('Z',''))

# ord_t(a,b) = True si 'b' es posterior a 'a', False si no
# 'a' y 'b' tienen la forma '2010-10-17T01:48:53Z'
def ord_t(a,b):
    a = numb(a)
    b = numb(b)
    if a <= b:
        return True
    else:
        return False

users = list(set(df[0]))
# t0 = principio de los tiempos, asumiendo que los checkins ya vienen
# ordenados del mas reciente al mas antiguo
t0 = time.time()
time0 = min(numb(df.loc[df[0]==u].iloc[-1][1]) for u in users[:1000])
print(time.time()-t0)

