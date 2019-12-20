import geopy.distance as geodist
import pandas as pd
# Me quedo con Nueva York porque tiene muchos checkins
# Quiero agarrar todos los checkins en un radio de 200 km desde el centro de NY
M = 3 #cantidad de meses
w_datos = pd.read_csv("works_{}meses.csv".format(M),index_col=0)
nw_datos = pd.read_csv("noworks_{}meses.csv".format(M),index_col=0)

w_xy = list(zip(w_datos["lat"],w_datos["long"]))
nw_xy = list(zip(nw_datos["lat"],nw_datos["long"]))

# Ponele que el centro de NY es el central park
# Coordenadas del central park:
centralpark = (40.7829,-73.9654)

# geodist.distance(x,y) = distancia en kilometros entre x e y
w_xy_NY = [p for p in w_xy if geodist.distance(centralpark,p)<200]
nw_xy_NY = [p for p in nw_xy if geodist.distance(centralpark,p)<200]


# Para leaflet---------------------------------------------------
"""
works_NY_tab = pd.DataFrame(w_xy_NY,columns=["lat","long"])
works_NY_tab.to_csv("works_NY_{}meses.csv".format(M))
noworks_NY_tab = pd.DataFrame(nw_xy_NY,columns=["lat","long"])
noworks_NY_tab.to_csv("noworks_NY_{}meses.csv".format(M))
"""
#----------------------------------------------------------------

df = pd.read_csv('checkins_{}meses.csv'.format(M),header=0,index_col=0,
    names=["user","time","lat","long","loc_id"])
df["time"] = pd.to_datetime(df["time"])

w_df = dict()
for w in w_xy_NY:
    x,y = w
    d = df.loc[df["lat"]==x].loc[df["long"]==y]
    w_df[w] = d

nw_df = dict()
for nw in nw_xy_NY:
    x,y = nw
    d = df.loc[df["lat"]==x].loc[df["long"]==y]
    nw_df[nw] = d



#-----------------------------------------------------------------------

t_inicio = min(df["time"])
t_final = max(df["time"])

oneweek = pd.Timedelta("7 days")

otrasemana = [t_inicio]
t = t_inicio
while t < t_final:
    t += oneweek
    otrasemana.append(t)

semanas = list(zip(otrasemana[:-1],otrasemana[1:]))

#nw_week_people_times = {lugares (no trabajos): {semanas: {personas que fueron esa semana: lista de times en los que fueron}}}
#Esto tarda tiempo...
nw_week_people_times = dict()
for nw in nw_df.keys():
    nw_week_people_times[nw] = dict()
    i = 0
    for s in semanas:
        S = "Semana {}".format(i)
        i += 1
        nw_week_people_times[nw][S] = dict()
        fake_lunes = s[0]
        fake_domingo = s[1]
        dnw = nw_df[nw]
        d = dnw.loc[(dnw["time"]>=fake_lunes)&(dnw["time"]<fake_domingo)]
        people = set(d["user"])
        for p in people:
            nw_week_people_times[nw][S][p] = list(d["time"])

#nw_week_ncheck = {lugares (no trabajos): {semanas: cantidad de checkins esa semana}}
nw_week_ncheck = dict()
i = 0
for nw in nw_week_people_times.keys():
    nw_week_ncheck[nw] = dict()
    for s in nw_week_people_times[nw].keys():
        c = 0
        for p in nw_week_people_times[nw][s].keys():
            c += len(nw_week_people_times[nw][s][p])
        nw_week_ncheck[nw][s] = c

MAX = max(max(nw_week_ncheck[lug].values()) for lug in nw_week_ncheck.keys())

nsemanas = ["Semana {}".format(i) for i in range(len(semanas))]

import colorsys
import math

def grow(inicio,fin,r,f):
    R = r**(1/f)
    return inicio + R*(fin-inicio)

for s in nsemanas:
    datos = []
    MAX = max(nw_week_ncheck[lugar][s] for lugar in nw_week_ncheck.keys())
    if MAX==0:
        continue
    for nw in nw_week_ncheck.keys():
        x,y = nw
        n = nw_week_ncheck[nw][s]
        if n==0:
            continue
        r = n/MAX
        hue,sat,val = grow(2/3,1,r,2), 1, 1
        opac = grow(0.4,1,r,2)
        rad = grow(1,10,r,2)
        C = "#%02x%02x%02x" % tuple(map(lambda x:math.floor(255*x),colorsys.hsv_to_rgb(hue,sat,val)))
        datos.append([x,y,C,opac,rad,n])
    tab = pd.DataFrame(datos,columns=["lat","long","color","opacidad","radio","checkins"])
    tab.to_csv("NY_3meses/nw_NY_{}meses_{}.csv".format(M,s))


