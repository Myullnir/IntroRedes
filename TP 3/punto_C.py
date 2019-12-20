import igraph
import networkx as nx
import matplotlib.pyplot as plt
from func import clusterize
import numpy as np

G = nx.read_gml("dolphins.gml")



# Infomap
GI = clusterize(G)
nx.draw_networkx(G,node_color = list(GI.values()),
	               with_labels = False)
# Fast Greedy
GFG = clusterize(G,method="fastgreedy")
nx.draw_networkx(G,node_color = list(GFG.values()),
	               with_labels = False)

# Louvain
GL = clusterize(G,method="louvain")
nx.draw_networkx(G,node_color = list(GL.values()),
	               with_labels = False)

# Edge Betweenness
GE = clusterize(G,method="edge_betweenness")
nx.draw_networkx(G,node_color = list(GE.values()),
	               with_labels = False)

Dic=[GI,GFG,GL,GE]
Lab=["Infomap","Fast-Greedy","Louvain","Edge-Betweennes"]


# Plot:
#plt.show()

# Punto C

Nnodos = len(G.nodes())

for cl1 in range(len(Dic)):
    for cl2 in range(cl1,len(Dic)):
        if cl1!=cl2:
            # Armamos las listas 1 y 2 de delfines segun comunidad
            #------------------------------------------------------
            Ncom = max(Dic[cl1].values())+1
            L0=[]
            for k in range(Ncom):
                L = [x for x in Dic[cl1].keys() if k == Dic[cl1][x]]
                L0.append(L)
            Ncom = max(Dic[cl2].values())+1
            L1=[]
            for k in range(Ncom):
                L = [x for x in Dic[cl2].keys() if k == Dic[cl2][x]]
                L1.append(L)
            # Ahora armemosla matriz de coocurrencia
            n0 = len(L0)
            n1 = len(L1)
            M_co = np.ones((n0,n1))
            for m in range(n0):
                for p in range(n1):
                    M_co[m][p] = len(set(L0[m]).intersection(set(L1[p])))
            P_co = M_co/Nnodos
            #-------------------------------------------------------
            # Probabilidades de los clusters de la lista 0
            P_c0 = []
            for i in range(n0):
                p=len(L0[i])/Nnodos
                P_c0.append(p)
            # Probabilidades de los clusters de la lista 1
            P_c1 = []
            for i in range(n1):
                p=len(L1[i])/Nnodos
                P_c1.append(p)
            #IM = sum(sum(P_co[i][j]*np.log(P_co[i][j]/(P_c0[i]*P_c1[j])) for i in range(n0)) for j in range(n1) if P_co[i][j]!=0)
            IM = 0
            for i in range(n0):
                for j in range(n1):
                    if P_co[i][j]!=0:
                        IM += P_co[i][j]*np.log(P_co[i][j]/(P_c0[i]*P_c1[j]))
            # Entropía de Shannon
            H0= sum([-x*np.log(x) for x in P_c0])
            H1= sum([-x*np.log(x) for x in P_c1])
            ImN = 2*IM/(H0+H1)
            print("La informacion mutua entre las particiones {} y {} es {}".format(Lab[cl1],Lab[cl2],ImN))
            # Imagino que ya tengo L0 y L1
            Nod = list(G.nodes())
            M_pre=np.zeros((2,2))
            Mam=[]
            for x in Nod:
                Mam.append(x)
                for y in Nod:
                    if y not in Mam:
                        if Dic[cl1][x]==Dic[cl1][y]:
                            if Dic[cl2][x]==Dic[cl2][y]:
                                M_pre[0][0] += 1
                            else:
                                M_pre[0][1] += 1
                        else:
                            if Dic[cl2][x]==Dic[cl2][y]:
                                M_pre[1][0] += 1
                            else:
                                M_pre[1][1] += 1
            Prc = (M_pre[0][0]+M_pre[1][1])/(Nnodos*(Nnodos-1)/2)
            print("La precision entre las particiones {} y {} es {}".format(Lab[cl1],Lab[cl2],Prc))
