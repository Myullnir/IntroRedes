import pandas as pd
import time

db = pd.read_csv('checkins_3meses.csv',header=0,index_col=0)
users = set(db['0'])


def ldata(archive):
        f = open(archive)
        data = []
        for line in f:
            col = line.split("\t")
            col = {int(x.strip()) for x in col}
            data.append(col)
        return data


edges = ldata('Brightkite_edges.txt')

for e in edges:
    if 
