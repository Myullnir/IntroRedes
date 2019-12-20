#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import time


#--------------------------- Checkins -------------------------------------------

M = int(input("¿Cuántos meses querés?: ")) # cantidad de meses
#M = 6

file = "loc-brightkite_totalCheckins.txt"
# Si no funciona:
# file = "Brightkite_totalCheckins.txt"
df = pd.read_csv(file,header=0,sep="\t",
    names=["user","check-in_time","latitude","longitude","location_id"])

df["check-in_time"] = pd.to_datetime(df["check-in_time"])

tfinal = pd.to_datetime("2008-03") + pd.Timedelta("{} days".format(30*M))

primeros_meses = df["check-in_time"] < tfinal
df_filtrado = df.loc[primeros_meses]

# Limpiemos las islas (0,0) y las latitudes fuera de rango:
#df_filtrado["latitude"] = pd.to_numeric(df_filtrado["latitude"])
#df_filtrado["longitude"] = pd.to_numeric(df_filtrado["longitude"])
df_filtrado = df_filtrado.loc[~((df_filtrado["latitude"] == 0) & (df_filtrado["longitude"] == 0))]
df_filtrado = df_filtrado.loc[(-90 < df_filtrado["latitude"]) & (df_filtrado["latitude"] < 90)]


df_filtrado.to_csv("checkins_{}meses.csv".format(M),sep="\t",
    columns=["user","check-in_time","latitude","longitude","location_id"])



#--------------------------- Edges ----------------------------------------------

users = set(df_filtrado["user"])

def lread(archive):
       f = open(archive)
       data = []
       for line in f:
           col = line.split("\t")
           col = frozenset(int(x.strip()) for x in col)
           data.append(col)
       return set(data)

edges = lread('Brightkite_edges.txt')
edges_filtrados = [list(e) for e in edges if len(e.intersection(users))==2]

with open("edges_{}meses.txt".format(M),"w") as f:
    for e in edges_filtrados:
        x,y = e
        f.write("{}\t{}\n".format(x,y))
