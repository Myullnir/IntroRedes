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

t0=time.time()


def ldata(archive):
        f = open(archive)
        data = []
        for line in f:
            col = line.split("\t")
            col = [x.strip() for x in col]
            data.append(col)
        return data 
    
#Amigos=ldata("Brightkite_edges.txt")
#Ubicacion=ldata("Brightkite_totalCheckins.txt")

#t1=time.time()
#tiempo=t1-t0
#print(tiempo)

for i in range(2000,2400):
    print(Ubicacion[i])
    

