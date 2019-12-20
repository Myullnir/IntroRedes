# El objetivo aca es obtener los lugares de trabajo y
# los hogares, y luego graficarlos en mapas

import time
t0 = time.time()

import itertools
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('checkins_3meses.csv',header=0,index_col=0,
    names=["user","check-in_time","latitude","longitude","location_id"])

df["check-in_time"] = pd.to_datetime(df["check-in_time"])

D = {}
for d in range(len(df)):
    if d%5000==0: print("Ya hice el {}%".format(100*d/len(df)))
    p = df.iloc[d][0]
    x = df.iloc[d][2]
    y = df.iloc[d][3]
    lugar = (x,y)
    try:
        D[p][lugar] += 1
    except:
        try:
            D[p][lugar] = 1
        except:
            D[p] = {lugar: 1}

# U_LC = {usuario: {lugar: cantidad de veces}}
U_LC = D
ULCworkers = {k:D[k] for k in D.keys() if len(D[k])>=2}
# u_housework = {usuario: [lugar1,lugar2]},
# para todos los usuarios con dos o mas checkins
u_housework = {}
for u in ULCworkers.keys():
    L = list(ULCworkers[u].items())
    L.sort(key=lambda x:x[1])
    u_housework[u] = [L[-1][0],L[-2][0]]

L0 = [x for t in u_housework.values() for x in t]
L = list(set(L0))
L.sort(key=lambda x:L0.count(x), reverse=True)

# Los workplaces van a ser de por lo menos 5 personas
works = []
i = 1
while L0.count(L[i])>=5:
    works.append(L[i])
    i+=1

# work_emp = {empresa: [empleados]}
work_emp = {}
for w in works:
    x = w[0]
    y = w[1]
    d = df.loc[df["latitude"]==x].loc[df["longitude"]==y]
    work_emp[w] = list(set(d["user"]))


# workemp_sort = [(empresa, [empleados])]
# ordenada desde la empresa mas grande a la mas chica
workemp_sort = sorted(list(work_emp.items()),key=lambda x:len(x[1]),reverse=True)

x_works, y_works = zip(*works)
# df_nowork son los checkins fuera de los lugares de trabajo
df_nowork = df.loc[~(df["latitude"].isin(x_works) & df["longitude"].isin(y_works))]
users_nowork = set(df_nowork["user"])

workers = {x for w in work_emp.values() for x in w}

# workaholics: solo hacen checkins en el trabajo (o trabajan en su casa)
workaholics = {w for w in workers if w not in users_nowork}

# saneworkers: trabajan pero no solo eso
saneworkers = workers.difference(workaholics)




"""
T0 = time.time()
G = nx.Graph()
pairs = itertools.combinations(work_emp[company],2)
for p in pairs:
    e1,e2 = p
    d1 = df_nowork.loc[df_nowork["user"]==e1]
    d2 = df_nowork.loc[df_nowork["user"]==e2]
    weight_p = 0
    for i in range(len(d1)):
        x1 = d1["latitude"].iloc[i]
        y1 = d1["longitude"].iloc[i]
        for j in range(len(d2)):
            x2 = d2["latitude"].iloc[j]
            y2 = d2["longitude"].iloc[j]
            if (x1,y1)==(x2,y2):
                t1 = d1["check-in_time"].iloc[i]
                t2 = d2["check-in_time"].iloc[j]
                if (t1-t2).__abs__()<pd.Timedelta('01:00:00'):
                    weight_p += 1
    G.add_edges_from([(e1,e2,{'weight':weight_p})])

print(time.time()-T0)





R = sorted(workers,key=lambda x:len(df_nowork.loc[df_nowork["user"]==x]["check-in_time"]))


"""



# work_graph = {empresa: grafo pesado de empleados segun sus salidas}
work_graph = {}
for company in work_emp.keys():
    G = nx.Graph()
    pairs = itertools.combinations(work_emp[company],2)
    for p in pairs:
        e1,e2 = p
        d1 = df_nowork.loc[df_nowork["user"]==e1]
        d2 = df_nowork.loc[df_nowork["user"]==e2]
        weight_p = 0
        for i in range(len(d1)):
            x1 = d1["latitude"].iloc[i]
            y1 = d1["longitude"].iloc[i]
            for j in range(len(d2)):
                x2 = d2["latitude"].iloc[j]
                y2 = d2["longitude"].iloc[j]
                if (x1,y1)==(x2,y2):
                    t1 = d1["check-in_time"].iloc[i]
                    t2 = d2["check-in_time"].iloc[j]
                    if (t1-t2).__abs__()<pd.Timedelta('01:00:00'):
                        weight_p += 1
        G.add_edges_from([(e1,e2,{'weight':weight_p})])
    work_graph[company] = G


